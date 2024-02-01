import ast
import logging
import os
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from boa3.builtin.compile_time import NeoMetadata
from boa3.internal import constants
from boa3.internal.analyser import asthelper
from boa3.internal.analyser.astanalyser import IAstAnalyser
from boa3.internal.analyser.importanalyser import ImportAnalyser
from boa3.internal.analyser.model.ManifestSymbol import ManifestSymbol
from boa3.internal.analyser.model.functionarguments import FunctionArguments
from boa3.internal.analyser.model.optimizer import UndefinedType
from boa3.internal.analyser.model.symbolscope import SymbolScope
from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.model.builtin.builtin import Builtin
from boa3.internal.model.builtin.compile_time.neometadatatype import MetadataTypeSingleton
from boa3.internal.model.builtin.decorator import ContractDecorator
from boa3.internal.model.builtin.decorator.builtindecorator import IBuiltinDecorator
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.callable import Callable
from boa3.internal.model.decorator import IDecorator
from boa3.internal.model.event import Event
from boa3.internal.model.expression import IExpression
from boa3.internal.model.imports.importsymbol import BuiltinImport, Import
from boa3.internal.model.imports.package import Package
from boa3.internal.model.method import Method
from boa3.internal.model.module import Module
from boa3.internal.model.property import Property
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.annotation.metatype import MetaType
from boa3.internal.model.type.annotation.uniontype import UnionType
from boa3.internal.model.type.classes.classscope import ClassScope
from boa3.internal.model.type.classes.classtype import ClassType
from boa3.internal.model.type.classes.contractinterfaceclass import ContractInterfaceClass
from boa3.internal.model.type.classes.pythonclass import PythonClass
from boa3.internal.model.type.classes.userclass import UserClass
from boa3.internal.model.type.collection.icollection import ICollectionType as Collection
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.primitive.primitivetype import PrimitiveType
from boa3.internal.model.type.type import IType, Type
from boa3.internal.model.variable import Variable


class ModuleAnalyser(IAstAnalyser, ast.NodeVisitor):
    """
    This class is responsible for mapping the locals of the functions and modules

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.

    :ivar modules: a dictionary that maps each module with its name. Empty by default.
    :ivar symbols: a dictionary that maps the global symbols.
    """

    def __init__(self, analyser, symbol_table: Dict[str, ISymbol],
                 filename: str = None, root_folder: str = None,
                 analysed_files: Optional[dict] = None,
                 import_stack: Optional[List[str]] = None,
                 log: bool = False,
                 fail_fast: bool = True):
        super().__init__(analyser.ast_tree, filename, root_folder, log, fail_fast)
        self.modules: Dict[str, Module] = {}
        self.symbols: Dict[str, ISymbol] = symbol_table

        from boa3.internal.analyser.analyser import Analyser
        if isinstance(analysed_files, dict):
            for file_path, file_analyser in analysed_files.copy().items():
                fixed_path = file_path.replace(os.sep, constants.PATH_SEPARATOR)
                if file_path != fixed_path:
                    analysed_files.pop(file_path)
                    analysed_files[fixed_path] = file_analyser
        else:
            analysed_files = {}

        analysed_files[filename.replace(os.sep, constants.PATH_SEPARATOR)] = analyser
        self._analysed_files: Dict[str, Analyser] = analysed_files

        if isinstance(import_stack, list):
            import_stack = [file_path.replace(os.sep, constants.PATH_SEPARATOR)
                            if isinstance(file_path, str) else file_path
                            for file_path in import_stack]
        else:
            import_stack = []
        self._import_stack: List[str] = import_stack

        self._builtin_functions_to_visit: Dict[str, IBuiltinMethod] = {}
        self._current_module: Module = None
        self._current_class: UserClass = None
        self._current_method: Method = None
        self._current_event: Event = None

        self._deploy_method: Optional[Method] = None

        self._annotated_variables: List[str] = []
        self._global_assigned_variables: List[str] = []
        self._scope_stack: List[SymbolScope] = []

        self._metadata: NeoMetadata = None
        self._metadata_node: ast.AST = ast.parse('')
        self._manifest_symbols: Dict[Tuple[ManifestSymbol, str, int], Callable] = {}
        self.imported_nodes: List[ast.AST] = []

        if self.filename:
            self._tree.filename = self.filename
        self.analyse_visit(self._tree)

        analyser.metadata = self._metadata if self._metadata is not None else NeoMetadata()

    @property
    def _current_scope(self) -> Union[Method, Module, UserClass, None]:
        """
        Returns the scope that is currently being analysed

        :return: the current scope. Return None if it is the global scope
        :rtype: Method or Module or None
        """
        if self._current_method is not None:
            return self._current_method
        if self._current_class is not None:
            return self._current_class
        return self._current_module

    @property
    def _current_symbol_scope(self) -> Optional[SymbolScope]:
        if len(self._scope_stack) > 0:
            return self._scope_stack[-1]
        else:
            return None

    @property
    def global_symbols(self) -> Dict[str, ISymbol]:
        """
        Returns the symbols in global scope

        :return: the symbol table of the global scope
        """
        global_symbols: Dict[str, ISymbol] = {}

        global_symbols.update(self.symbols)
        for mod in self.modules.values():
            global_symbols.update(mod.symbols)

        return global_symbols

    @property
    def analysed_files(self) -> Dict[str, Any]:
        return self._analysed_files.copy()

    def __include_variable(self,
                           var_id: str, var_type_id: Union[str, IType],
                           source_node: ast.AST,
                           var_enumerate_type: IType = Type.none,
                           assignment: bool = True,
                           literal_value: Any = asthelper.INVALID_NODE_RESULT):
        """
        Includes the variable in the symbol table if the id was not used

        :param var_id: variable id
        :param var_type_id: variable type id
        :type var_type_id: str or IType
        :param var_enumerate_type: variable value type id if var_type_id is a SequenceType
        """
        if not isinstance(var_id, str) and isinstance(var_id, Iterable):
            variables = [var_name.id if isinstance(var_name, ast.Name) else self.visit(var_name).id
                         for var_name in source_node.targets[0].elts]
            var_types = self.visit(source_node.value)
        else:
            variables = [var_id]
            var_types = [var_type_id]

        for x in range(min(len(variables), len(var_types))):
            var_id, var_type_id = variables[x], var_types[x]

            outer_symbol = self.get_symbol(var_id)
            first_assign = outer_symbol is None
            if var_id in self._current_symbol_scope.symbols:
                if hasattr(outer_symbol, 'set_is_reassigned'):
                    is_module_scope = isinstance(self._current_scope, Module)
                    if not is_module_scope:
                        outer_symbol.set_is_reassigned()
                    elif isinstance(source_node, ast.AugAssign):
                        # augmented assignments of global variables shouldn't be evaluated in the module analyser
                        outer_symbol.set_is_reassigned()
                    self.__set_source_origin(source_node, is_module_scope)
            else:
                if (not isinstance(source_node, ast.Global) and
                        (not hasattr(source_node, 'targets') or not isinstance(source_node.targets[x], ast.Subscript))):
                    if outer_symbol is not None:
                        self._log_warning(
                            CompilerWarning.NameShadowing(source_node.lineno, source_node.col_offset, outer_symbol, var_id)
                        )
                        first_assign = True

                var_type = None
                if isinstance(var_type_id, SequenceType):
                    var_type = var_type_id
                    var_enumerate_type = self.get_enumerate_type(var_type)
                elif isinstance(var_type_id, IType):
                    var_type = var_type_id

                # when setting a None value to a variable, set the variable as any type
                if var_type is Type.none:
                    var_type = Type.any

                if isinstance(var_type, IType) or var_type is None:
                    # if type is None, the variable type depends on the type of a expression
                    if isinstance(source_node, ast.Global):
                        var = outer_symbol
                    else:
                        if isinstance(var_type, SequenceType):
                            var_type = var_type.build_collection(var_enumerate_type)
                        var = Variable(var_type, origin_node=source_node)

                    if first_assign and isinstance(Type.get_type(literal_value), PrimitiveType):
                        var.set_initial_assign(literal_value)

                    self._current_symbol_scope.include_symbol(var_id, var)
                    if isinstance(source_node, ast.AnnAssign):
                        self._annotated_variables.append(var_id)
            if hasattr(self._current_scope, 'assign_variable') and assignment:
                self._global_assigned_variables.append(var_id)

    def __include_callable(self, callable_id: str, callable: Callable):
        """
        Includes the method in the symbol table if the id was not used

        :param callable_id: method id
        :param callable: method to be included
        """
        if ((self._current_scope is self._current_class or callable_id not in self._current_scope.symbols)
                and hasattr(self._current_scope, 'include_callable')):
            already_exists = not self._current_scope.include_callable(callable_id, callable)
        else:
            symbol = self.get_symbol(callable_id)
            already_exists = symbol is not None and not isinstance(symbol, IBuiltinMethod)

        if already_exists:
            self._log_error(CompilerError.DuplicatedIdentifier(callable.origin.lineno,
                                                               callable.origin.col_offset,
                                                               callable_id))

        if callable.is_public:
            # check if the external name + argument number is unique
            manifest_name = callable.external_name if callable.external_name is not None else callable_id
            manifest_id = (ManifestSymbol.get_manifest_symbol(callable), manifest_name, len(callable.args))

            if manifest_id in self._manifest_symbols:
                self._log_error(CompilerError.DuplicatedManifestIdentifier(callable.origin.lineno,
                                                                           callable.origin.col_offset,
                                                                           manifest_name, len(callable.args)
                                                                           ))
            else:
                self._manifest_symbols[manifest_id] = callable

    def __include_class_variable(self, cl_var_id: str, cl_var: Variable):
        """
        Includes the class variable in the current class

        :param cl_var_id: variable name
        :param cl_var: variable to be included
        """
        if cl_var_id not in self._current_scope.class_variables:
            self._current_class.include_symbol(cl_var_id, cl_var, ClassScope.CLASS)

    def __set_source_origin(self, source_node: ast.AST, scope_is_correct: bool = True):
        if scope_is_correct or self._current_scope == self._deploy_method:
            source_node.origin = self._tree

    def get_symbol(self, symbol_id: str,
                   is_internal: bool = False,
                   check_raw_id: bool = False,
                   origin_node: ast.AST = None) -> Optional[ISymbol]:
        for scope in reversed(self._scope_stack):
            if symbol_id in scope.symbols:
                return scope.symbols[symbol_id]

            if check_raw_id:
                found_symbol = self._search_by_raw_id(symbol_id, list(scope.symbols.values()))
                if found_symbol is not None:
                    return found_symbol

        if symbol_id in self._current_scope.symbols:
            # the symbol exists in the local scope
            return self._current_scope.symbols[symbol_id]
        elif symbol_id in self._current_module.symbols:
            # the symbol exists in the module scope
            return self._current_module.symbols[symbol_id]

        if check_raw_id:
            found_symbol = self._search_by_raw_id(symbol_id, list(self._current_scope.symbols.values()))
            if found_symbol is not None:
                return found_symbol

            found_symbol = self._search_by_raw_id(symbol_id, list(self._current_module.symbols.values()))
            if found_symbol is not None:
                return found_symbol

        return super().get_symbol(symbol_id, is_internal, check_raw_id, origin_node)

    def get_annotation(self, value: Any, use_metatype: bool = False, accept_none: bool = False) -> Optional[IType]:
        if not isinstance(value, ast.AST):
            return None

        annotation_type = self.get_type(value, use_metatype)
        if not isinstance(annotation_type, PythonClass):
            return annotation_type
        if hasattr(value, 'value') and value.value is None and annotation_type is Type.none:
            return annotation_type

        if isinstance(value, (ast.Constant, ast.NameConstant, ast.List, ast.Tuple, ast.Dict, ast.Set)):
            # annotated types should only accept types
            return None
        return annotation_type

    def _check_annotation_type(self, node: ast.AST, origin_node: Optional[ast.AST] = None):
        if node is None:
            return

        if origin_node is None:
            origin_node = node

        if self.get_annotation(node) is None:
            actual_type = self.get_type(node)
            self._log_error(
                CompilerError.MismatchedTypes(
                    origin_node.lineno, origin_node.col_offset,
                    expected_type_id=type.__name__,
                    actual_type_id=actual_type.identifier
                ))

    # region Log

    def _log_import(self, import_from: str):
        if self._log:
            logging.getLogger(constants.BOA_LOGGING_NAME).info("Importing '{0}'\t <{1}>".format(import_from, self.filename))

    def _log_unresolved_import(self, origin_node: ast.AST, import_id: str):
        if self._log:
            self._log_error(
                CompilerError.UnresolvedReference(
                    line=origin_node.lineno,
                    col=origin_node.col_offset,
                    symbol_id=import_id
                )
            )

    # endregion

    # region Metadata

    def _read_metadata_object(self, function: ast.FunctionDef):
        """
        Gets the metadata object defined in this function

        :param function:
        """
        if self._metadata is not None:
            # metadata function has been defined already
            self._log_warning(
                CompilerWarning.RedeclaredSymbol(
                    line=function.lineno, col=function.col_offset,
                    symbol_id=Builtin.Metadata.identifier
                )
            )
        # this function must have a return and no arguments
        elif len(function.args.args) != 0:
            self._log_error(
                CompilerError.UnexpectedArgument(
                    line=function.lineno, col=function.col_offset
                )
            )
        elif not any(isinstance(stmt, ast.Return) for stmt in function.body):
            self._log_error(
                CompilerError.MissingReturnStatement(
                    line=function.lineno, col=function.col_offset,
                    symbol_id=function.name
                )
            )
        else:
            function.returns = None
            function.decorator_list = []

            imports: List[ast.AST] = []
            other_instructions: List[ast.AST] = []
            for node in self._tree.body:
                if node == function:
                    # metadata function must be right after all the imports, so it executes correctly
                    continue

                if isinstance(node, (ast.ImportFrom, ast.Import)):
                    imports.append(node)
                else:
                    other_instructions.append(node)

            module: ast.Module = ast.parse('')
            module.body = imports + [function] + other_instructions
            ast.copy_location(module, function)
            namespace = {}

            import sys
            file_dir = os.path.abspath(os.path.dirname(self.filename))
            sys_path = sys.path.copy()

            try:
                from boa3.internal import utils
                if os.path.abspath(self.root_folder) != file_dir:
                    sc_paths = [os.path.abspath(self.root_folder), file_dir]
                else:
                    sc_paths = [file_dir]

                sys.path = sc_paths + utils.list_inner_packages(file_dir) + sys_path

                # executes the function
                code = compile(module, filename='<boa3>', mode='exec')
                exec(code, namespace)
            except ModuleNotFoundError:
                # will fail if any imports can't be executed
                # in this case, the error is already logged
                return
            except BaseException as inner_exception:
                # reordering the module tree may raise unexpected exceptions
                # ignore if it has generated the metadata function
                if function.name not in namespace:
                    raise inner_exception
            finally:
                sys.path = sys_path

            obj: Any = namespace[function.name]()
            node: ast.AST = function.body[-1] if len(function.body) > 0 else function
            # return must be a NeoMetadata object
            if not isinstance(obj, NeoMetadata):
                obj_type = self.get_type(obj).identifier if self.get_type(obj) is not Type.any else type(obj).__name__
                self._log_error(
                    CompilerError.MismatchedTypes(
                        line=node.lineno, col=node.col_offset,
                        expected_type_id=NeoMetadata.__name__,
                        actual_type_id=obj_type
                    )
                )
                return

            # validate if the extras field can be converted to json
            try:
                import json
                json.dumps(obj.extras)
            except BaseException as e:
                self._log_error(
                    CompilerError.InvalidType(
                        line=node.lineno, col=node.col_offset,
                        symbol_id=str(e)
                    )
                )
                return

            # validates the metadata attributes types
            attributes: Dict[str, Any] = {attr: value
                                          for attr, value in dict(obj.__dict__).items()
                                          if attr in Builtin.metadata_fields}
            if any(not isinstance(value, Builtin.metadata_fields[attr]) for attr, value in attributes.items()):
                for expected, actual in [(Builtin.metadata_fields[attr], type(v_type))
                                         for attr, v_type in attributes.items()
                                         if not isinstance(v_type, Builtin.metadata_fields[attr])]:
                    if isinstance(expected, Iterable):
                        expected_id = 'Union[{0}]'.format(', '.join([tpe.__name__ for tpe in expected]))
                    elif hasattr(expected, '__name__'):
                        expected_id = expected.__name__
                    else:
                        expected_id = str(expected)

                    self._log_error(
                        CompilerError.MismatchedTypes(
                            line=node.lineno, col=node.col_offset,
                            expected_type_id=expected_id,
                            actual_type_id=actual.__name__
                        )
                    )
            else:
                # if the function was defined correctly, sets the metadata object of the smart contract
                self._metadata = obj
                self._metadata_node = function  # for error messages only

    # endregion

    # region AST

    def visit_ImportFrom(self, import_from: ast.ImportFrom):
        """
        Includes methods and variables from other modules into the current scope

        :param import_from:
        """
        self._log_import(import_from.module)
        analyser = self._analyse_module_to_import(import_from, import_from.module)
        if analyser is not None:
            import_alias: Dict[str] = \
                {alias.name: alias.asname if alias.asname is not None else alias.name for alias in import_from.names}

            new_symbols: Dict[str, ISymbol] = analyser.export_symbols(list(import_alias.keys()))

            # check if the wildcard is used and filter the symbols
            if constants.IMPORT_WILDCARD in import_alias:
                import_alias.pop(constants.IMPORT_WILDCARD)
                for imported_symbol_id in new_symbols:
                    # add the symbols imported with the wildcard without specific aliases in the dict
                    if imported_symbol_id not in import_alias:
                        import_alias[imported_symbol_id] = imported_symbol_id

            # includes the module to be able to generate the functions
            imported_module = self._build_import(analyser.path, analyser.tree, analyser, import_alias)
            self._current_scope.include_symbol(import_from.module, imported_module)

            for name, alias in import_alias.items():
                if name in new_symbols:
                    self._current_scope.include_symbol(alias, imported_module.symbols[name])
                else:
                    # if there's a symbol that couldn't be loaded, log a compiler error
                    self._log_unresolved_import(import_from, name)

    def visit_Import(self, import_node: ast.Import):
        """
        Includes methods and variables from other modules into the current scope

        :param import_node:
        """
        import_alias: Dict[str] = \
            {alias.name: alias.asname if alias.asname is not None else alias.name for alias in import_node.names}

        for target, alias in import_alias.items():
            self._log_import(target)
            analyser = self._analyse_module_to_import(import_node, target)
            if analyser is not None:
                new_symbols: Dict[str, ISymbol] = analyser.export_symbols()
                for symbol in [symbol for symbol in analyser.symbols if symbol not in new_symbols]:
                    # if there's a symbol that couldn't be loaded, log a compiler error
                    self._log_unresolved_import(import_node, '{0}.{1}'.format(target, symbol))

                imported_module = self._build_import(analyser.path, analyser.tree, analyser)
                self._current_scope.include_symbol(alias, imported_module)

    def _build_import(self, origin: str, syntax_tree: ast.AST,
                      import_analyser: ImportAnalyser,
                      imported_symbols: Dict[str, ISymbol] = None) -> Import:

        if import_analyser.is_builtin_import:
            return BuiltinImport(origin, syntax_tree, import_analyser, imported_symbols)

        return Import(origin, syntax_tree, import_analyser, imported_symbols)

    def _analyse_module_to_import(self, origin_node: ast.AST, target: str) -> Optional[ImportAnalyser]:
        already_imported = {imported.origin: imported.analyser
                            for imported in self._current_module.symbols.values()
                            if isinstance(imported, Import) and imported.analyser is not None
                            }
        already_imported.update(self._analysed_files)

        try:
            analyser = ImportAnalyser(import_target=target,
                                      root_folder=self.root_folder,
                                      importer_file=self.filename,
                                      already_imported_modules=already_imported,
                                      import_stack=self._import_stack.copy(),
                                      log=self._log,
                                      fail_fast=self._fail_fast)

            if analyser.recursive_import:
                self._log_error(
                    CompilerError.CircularImport(line=origin_node.lineno,
                                                 col=origin_node.col_offset,
                                                 target_import=target,
                                                 target_origin=self.filename)
                )

            elif not analyser.can_be_imported:
                circular_import_error = next((error for error in analyser.errors
                                              if isinstance(error, CompilerError.CircularImport)),
                                             None)

                if circular_import_error is not None:
                    # if the problem was a circular import, the error was already logged
                    self.errors.append(circular_import_error)
                elif hasattr(analyser, 'is_namespace_package') and analyser.is_namespace_package:
                    return analyser
                else:
                    self._log_unresolved_import(origin_node, target)

            else:
                analyser.update_external_analysed_files(self._analysed_files)
                return analyser

        except CompilerError.CompilerError as error_on_import:
            if self._log:
                self.errors.append(error_on_import)
                raise error_on_import
            else:
                self._log_error(error_on_import)

    def visit_Module(self, module: ast.Module):
        """
        Visitor of the module node

        Fills module symbol table

        :param module:
        """
        mod: Module = Module()
        self._current_module = mod
        self._scope_stack.append(SymbolScope())

        global_stmts = []
        function_stmts = []
        for stmt in module.body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_stmts.append(stmt)
            elif not (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant)):
                # don't evaluate constant expression - for example: string for documentation
                if self.visit(stmt) is not Builtin.Event:
                    global_stmts.append(stmt)

        module.body = global_stmts + function_stmts
        for var_id, var in mod.variables.items():
            # all static fields must be initialized
            if not mod.is_variable_assigned(var_id):
                self._log_error(
                    CompilerError.UnresolvedReference(
                        line=var.origin.lineno if var.origin is not None else 0,
                        col=var.origin.col_offset if var.origin is not None else 0,
                        symbol_id=var_id
                    )
                )

        for stmt in function_stmts:
            result = self.visit(stmt)
            # don't evaluate the metadata function in the following analysers
            if result is Builtin.Metadata:
                module.body.remove(stmt)

        self.modules['main'] = mod
        module_scope = self._scope_stack.pop()
        for symbol_id, symbol in module_scope.symbols.items():
            if symbol_id in self._global_assigned_variables:
                mod.include_symbol(symbol_id, symbol)
                mod.assign_variable(symbol_id)

        self._global_assigned_variables.clear()
        self._current_module = None

    def visit_ClassDef(self, class_node: ast.ClassDef):
        """
        Visitor of the class node

        Includes the class in the scope of its module
        """
        bases = []
        for base in class_node.bases:
            base_type_id: Any = ast.NodeVisitor.visit(self, base)
            if isinstance(base_type_id, ast.Name):
                base_type_id = base_type_id.id

            base_symbol = self.get_symbol(base_type_id)
            # TODO: change when class inheritance with builtin types is implemented #2kq1ght
            if not isinstance(base_symbol, UserClass):
                self._log_error(
                    CompilerError.NotSupportedOperation(
                        class_node.lineno, class_node.col_offset,
                        symbol_id='class inheritance with builtins'
                    )
                )
            bases.append(base_symbol)

        # TODO: change when class inheritance with multiple bases is implemented #2kq1gmc
        if len(bases) > 1:
            self._log_error(
                CompilerError.NotSupportedOperation(
                    class_node.lineno, class_node.col_offset,
                    symbol_id='class inheritance with multiple bases'
                )
            )

        # TODO: change when base classes with keyword is implemented #2kq1gqy
        if len(class_node.keywords) > 0:
            self._log_error(
                CompilerError.NotSupportedOperation(
                    class_node.lineno, class_node.col_offset,
                    symbol_id='class keyword'
                )
            )

        # TODO: change when class decorators are implemented #2ewf04r
        class_decorators: List[Method] = self._get_decorators(class_node)
        if not all(isinstance(decorator, IBuiltinDecorator) and decorator.is_class_decorator
                   for decorator in class_decorators):
            # only builtin decorator are currently accepted
            self._log_error(
                CompilerError.NotSupportedOperation(
                    class_node.lineno, class_node.col_offset,
                    symbol_id='class decorator'
                )
            )

        contract_interface_decorator = next((decorator for decorator in class_decorators
                                             if isinstance(decorator, ContractDecorator)),
                                            None)

        if contract_interface_decorator is not None:
            from boa3.internal.model.type.classes.contractinterfaceclass import ContractInterfaceClass
            user_class = ContractInterfaceClass(contract_hash=contract_interface_decorator.contract_hash,
                                                identifier=class_node.name,
                                                decorators=class_decorators,
                                                bases=bases)
        else:
            user_class = UserClass(identifier=class_node.name,
                                   decorators=class_decorators,
                                   bases=bases)

        self._current_class = user_class
        if self._current_symbol_scope is not None:
            self._current_symbol_scope.include_symbol(class_node.name, user_class)
        self._scope_stack.append(SymbolScope())

        for stmt in class_node.body:
            self.visit(stmt)

        class_scope = self._scope_stack.pop()
        self._current_module.include_class(class_node.name, user_class)
        self._current_class = None

    def visit_FunctionDef(self, function: ast.FunctionDef):
        """
        Visitor of the function node

        Includes the method in the scope of its module

        :param function:
        """
        fun_decorators: List[Method] = self._get_decorators(function)
        if Builtin.Metadata in fun_decorators:
            self._log_warning(
                CompilerWarning.DeprecatedSymbol(
                    function.lineno, function.col_offset,
                    symbol_id=Builtin.Metadata.identifier
                )
            )
            self._read_metadata_object(function)
            return Builtin.Metadata

        if any(decorator is None for decorator in fun_decorators):
            self._log_error(
                CompilerError.NotSupportedOperation(
                    function.lineno, function.col_offset,
                    symbol_id='decorator'
                )
            )

        valid_decorators: List[IDecorator] = []
        for decorator in fun_decorators:
            if isinstance(decorator, IDecorator):
                if not decorator.is_function_decorator:
                    self._log_error(
                        CompilerError.NotSupportedOperation(
                            function.lineno, function.col_offset,
                            symbol_id=f'"{decorator.identifier}" decorator with function'
                        )
                    )

                decorator.update_args(function.args, self._current_scope)
                valid_decorators.append(decorator)

            # TODO: remove when user-created decorators are implemented #86a19uwzn
            elif isinstance(decorator, Method):
                self._log_error(
                    CompilerError.NotSupportedOperation(
                        function.lineno, function.col_offset,
                        symbol_id='user-created decorators'
                    )
                )

        is_static_method = (isinstance(self._current_scope, ClassType)
                            and Builtin.StaticMethodDecorator in valid_decorators)
        is_instance_method = (isinstance(self._current_scope, ClassType)
                              and Builtin.ClassMethodDecorator not in valid_decorators
                              and not is_static_method)
        is_class_constructor = is_instance_method and function.name == constants.INIT_METHOD_ID

        external_function_name = None
        if isinstance(self._current_class, ContractInterfaceClass):
            if not is_static_method:
                self._log_error(CompilerError
                                .InvalidUsage(function.lineno, function.col_offset,
                                              "Only static methods are accepted when defining contract interfaces"
                                              ))
            else:
                display_name_decorator = next((decorator for decorator in valid_decorators
                                               if isinstance(decorator, type(Builtin.ContractMethodDisplayName))),
                                              None)
                if display_name_decorator is not None:
                    external_function_name = display_name_decorator.external_name

        if is_instance_method:
            if Builtin.InstanceMethodDecorator not in valid_decorators:
                valid_decorators.append(Builtin.InstanceMethodDecorator)

            if len(function.args.args) > 0 and function.args.args[0].annotation is None:
                # set annotation to the self method
                from boa3.internal.model import set_internal_call
                self_argument = function.args.args[0]
                self_annotation = self._current_class.identifier

                self_ast_annotation = ast.parse(self_annotation).body[0].value
                set_internal_call(self_ast_annotation)

                ast.copy_location(self_ast_annotation, self_argument)
                self_argument.annotation = self_ast_annotation

        if is_class_constructor:
            # __init__ method behave like class methods
            if Builtin.ClassMethodDecorator not in valid_decorators:
                valid_decorators.append(Builtin.ClassMethodDecorator)

        fun_args: FunctionArguments = self.visit(function.args)
        if function.returns is not None:
            fun_rtype_symbol = self.visit(function.returns)
            self._check_annotation_type(function.returns)
        else:
            fun_rtype_symbol = Type.none

        # TODO: remove when dictionary unpacking operator is implemented #2kq1hbr
        if function.args.kwarg is not None:
            self._log_error(
                CompilerError.NotSupportedOperation(
                    function.lineno, function.col_offset,
                    symbol_id='** variables'
                )
            )

        # TODO: remove when keyword-only arguments are implemented #2ewewtz
        if len(function.args.kwonlyargs) > 0:
            self._log_error(
                CompilerError.NotSupportedOperation(
                    function.lineno, function.col_offset,
                    symbol_id='keyword-only arguments'
                )
            )

        if isinstance(fun_rtype_symbol, str):
            symbol = self.get_symbol(fun_rtype_symbol, origin_node=function.returns)
            if symbol is MetadataTypeSingleton:
                self._read_metadata_object(function)
                return Builtin.Metadata

            fun_rtype_symbol = self.get_type(symbol)

        fun_return: IType = self.get_type(fun_rtype_symbol)

        method = Method(args=fun_args.args, defaults=function.args.defaults, return_type=fun_return,
                        vararg=fun_args.vararg,
                        origin_node=function,
                        is_public=any(isinstance(decorator, type(Builtin.Public)) for decorator in fun_decorators),
                        decorators=valid_decorators,
                        external_name=external_function_name,
                        is_init=is_class_constructor)

        # debug information
        method.file_origin = self.filename.replace(os.path.sep, constants.PATH_SEPARATOR)

        if function.name in Builtin.internal_methods:
            internal_method = Builtin.internal_methods[function.name]
            if not internal_method.is_valid_deploy_method(method):
                self._log_error(
                    CompilerError.InternalIncorrectSignature(line=function.lineno,
                                                             col=function.col_offset,
                                                             expected_method=internal_method)
                )
        if function.name == constants.DEPLOY_METHOD_ID:
            self._deploy_method = method

        self._current_method = method
        self._scope_stack.append(SymbolScope())

        # don't evaluate constant expression - for example: string for documentation
        function.body = [stmt for stmt in function.body
                         if not (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant))]

        if isinstance(self._current_class, ClassType):
            method.origin_class = self._current_class
            if self._current_class.is_interface and len(function.body) > 0:
                first_instruction = function.body[0]
                if not isinstance(first_instruction, ast.Pass):
                    self._log_warning(CompilerWarning.UnreachableCode(first_instruction.lineno,
                                                                      first_instruction.col_offset))

        for stmt in function.body:
            self.visit(stmt)

        method_scope = self._scope_stack.pop()
        global_scope_symbols = self._scope_stack[0].symbols if len(self._scope_stack) > 0 else {}

        self._set_instance_variables(method_scope)
        self._set_properties(function)

        self._current_method = None
        self.__include_callable(function.name, method)

        for var_id, var in method_scope.symbols.items():
            if isinstance(var, Variable) and var_id not in self._annotated_variables:
                method.include_variable(var_id, Variable(UndefinedType, var.origin))
            else:
                method.include_symbol(var_id, var)

        self._annotated_variables.clear()

    def _get_decorators(self, node: ast.AST) -> List[Method]:
        """
        Gets a list of the symbols used to decorate the given node

        :param node: python ast node
        :return: a list with all decorators in the node. Empty if no decorator is found.
        """
        decorators = []
        if hasattr(node, 'decorator_list'):
            for decorator in node.decorator_list:
                decorator_visit = self.visit(decorator)
                if decorator_visit is None and hasattr(decorator, 'func'):
                    decorator_visit = self.visit(decorator.func)

                symbol = self.get_symbol(decorator_visit, origin_node=decorator)
                if hasattr(symbol, 'build'):
                    symbol = symbol.build(decorator, self)
                decorators.append(symbol)

        return decorators

    def _set_instance_variables(self, scope: SymbolScope):
        if (isinstance(self._current_class, UserClass)
                and isinstance(self._current_method, Method)
                and self._current_method.is_init
                and len(self._current_method.args) > 0):

            self_id = list(self._current_method.args)[0]
            for var_id, var in scope.symbols.items():
                if var_id.startswith(self_id):
                    split_name = var_id.split(constants.ATTRIBUTE_NAME_SEPARATOR)
                    if len(split_name) > 0:
                        instance_var_id = split_name[1]
                        self._current_class.include_symbol(instance_var_id, var)
                        scope.remove_symbol(var_id)

    def _set_properties(self, function: ast.FunctionDef):
        from boa3.internal.model.builtin.decorator import PropertyDecorator
        if (isinstance(self._current_class, UserClass)
                and isinstance(self._current_method, Method)
                and any(isinstance(decorator, PropertyDecorator) for decorator in self._current_method.decorators)):
            if len(self._current_method.args) < 1 or not any('self' == arg for arg in self._current_method.args):
                self._log_error(
                    CompilerError.SelfArgumentError(function.lineno, function.col_offset)
                )
            self._current_class.include_symbol(self._current_method.origin.name, Property(self._current_method))

    def visit_arguments(self, arguments: ast.arguments) -> FunctionArguments:
        """
        Visitor of the function arguments node

        :param arguments:
        :return: a dictionary that maps each argument to its identifier
        """
        fun_args = FunctionArguments()

        for arg in arguments.args:
            var_id, var = self.visit_arg(arg)  # Tuple[str, Variable]
            fun_args.add_arg(var_id, var)

        if arguments.vararg is not None:
            var_id, var = self.visit_arg(arguments.vararg)  # Tuple[str, Variable]
            fun_args.set_vararg(var_id, var)

        if arguments.kwarg is not None:
            var_id, var = self.visit_arg(arguments.kwarg)  # Tuple[str, Variable]
            fun_args.add_kwarg(var_id, var)

        return fun_args

    def visit_arg(self, arg: ast.arg) -> Tuple[str, Variable]:
        """
        Visitor of a function argument node

        :param arg:
        :return: a tuple with the identifier and the argument
        """
        var_id = arg.arg
        var_type: IType = self.get_type(arg.annotation)

        if var_type is Type.none and isinstance(arg.annotation, ast.Name):
            var_symbol: ISymbol = self.get_symbol(arg.annotation.id, origin_node=arg)
            var_type = self.get_type(var_symbol)

        self._check_annotation_type(arg.annotation, origin_node=arg)

        return var_id, Variable(var_type)

    def visit_Return(self, ret: ast.Return):
        """
        Visitor of the function return node

        If the return is a name, verifies if the symbol is defined

        :param ret: the python ast return node
        """
        if isinstance(ret.value, ast.Name):
            symbol_id = self.visit(ret.value)
            symbol = self.get_symbol(symbol_id)
            if symbol is None:
                # the symbol doesn't exist
                self._log_error(
                    CompilerError.UnresolvedReference(ret.value.lineno, ret.value.col_offset, symbol_id)
                )

        if ret.value is not None:
            self.__set_source_origin(ret.value)

    def visit_type(self, target: ast.AST) -> Optional[IType]:
        """
        Gets the type by its identifier

        :param target: ast node to be evaluated
        :return: the type of the value inside the node. None by default
        """
        target_type = self.visit(target)  # Type:str or IType
        if isinstance(target_type, str) and not isinstance(target, ast.Str):
            symbol = self.get_symbol(target_type)
            if symbol is None:
                # the symbol doesn't exist
                self._log_error(
                    CompilerError.UnresolvedReference(target.lineno, target.col_offset, target_type)
                )
            target_type = symbol

        if target_type is None and not isinstance(target, ast.NameConstant):
            # the value type is invalid
            return None

        if not isinstance(target_type, (ast.AST, IType, IExpression)) and isinstance(target_type, ISymbol):
            self._log_error(
                CompilerError.UnresolvedReference(
                    line=target.lineno, col=target.col_offset,
                    symbol_id=str(target_type)
                )
            )

        if isinstance(target_type, ClassType):
            init = target_type.constructor_method()
            if hasattr(init, 'build'):
                args = []
                if hasattr(target, 'args'):
                    for arg in target.args:
                        result = self.visit(arg)
                        if (isinstance(result, str) and not isinstance(arg, (ast.Str, ast.Constant))
                                and result in self._current_scope.symbols):
                            result = self.get_type(self._current_scope.symbols[result])
                        args.append(result)

                init = init.build(args)
            target_type = init.return_type if init is not None else target_type

        return self.get_type(target_type)

    def get_enumerate_type(self, var_type: IType) -> IType:
        return var_type.value_type if isinstance(var_type, SequenceType) else Type.none

    def visit_Assign(self, assign: ast.Assign):
        """
        Visitor of the variable assignment node

        Includes the variable in its scope if it's the first use

        :param assign:
        """
        # multiple assignments
        if isinstance(assign.targets[0], ast.Tuple):
            self._log_error(
                CompilerError.NotSupportedOperation(assign.lineno, assign.col_offset, 'Multiple variable assignments')
            )

        elif isinstance(assign.targets[0], ast.Subscript) and isinstance(assign.targets[0].slice, ast.Slice):
            self._log_error(
                CompilerError.NotSupportedOperation(assign.lineno, assign.col_offset, 'Assigning a value into a slice')
            )

        else:
            return self._visit_assign_value(assign)

    def _visit_assign_value(self, assign: ast.Assign | ast.AugAssign) -> IType:
        targets = assign.targets if isinstance(assign, ast.Assign) else [assign.target]
        var_type = self.visit_type(assign.value)

        if var_type is Type.none and isinstance(assign.value, ast.Name):
            symbol = self.get_symbol(assign.value.id)
            if isinstance(symbol, Event):
                var_type = Builtin.Event
                self._current_event = symbol

        return_type = var_type
        for target in targets:
            var_id = self.visit(target)
            if not isinstance(var_id, ISymbol):
                return_type = self.assign_value(var_id, var_type,
                                                source_node=assign,
                                                literal_value=asthelper.literal_eval_node(assign.value))

        return return_type

    def visit_AnnAssign(self, ann_assign: ast.AnnAssign):
        """
        Visitor of the annotated variable assignment node

        Includes the variable in its scope if it's the first use

        :param ann_assign:
        """
        var_id: str = self.visit(ann_assign.target)
        var_type: IType = self.visit_type(ann_assign.annotation)
        if var_type is Builtin.Event:
            self.visit(ann_assign.value)

        self._check_annotation_type(ann_assign.annotation, ann_assign)

        # TODO: check if the annotated type and the value type are the same #86a1ctmwy
        return self.assign_value(var_id, var_type,
                                 source_node=ann_assign,
                                 assignment=ann_assign.value is not None,
                                 literal_value=asthelper.literal_eval_node(ann_assign.value)
                                 )

    def visit_AugAssign(self, aug_assign: ast.AugAssign):
        return self._visit_assign_value(aug_assign)

    def assign_value(self,
                     var_id: str,
                     var_type: IType,
                     source_node: ast.AST,
                     assignment: bool = True,
                     literal_value: Any = None) -> IType:

        if var_type is Builtin.Event and self._current_event is not None:
            if '' in self._current_module.symbols and self._current_module.symbols[''] is self._current_event:
                self._current_scope.callables[var_id] = self._current_scope.callables.pop('')
                self._current_event.name = var_id
            else:
                self._current_scope.callables[var_id] = self._current_event
            self._current_event = None
        else:
            if isinstance(self._current_scope, UserClass):
                var = Variable(var_type, source_node)
                self.__include_class_variable(var_id, var)
            else:
                self.__include_variable(var_id, var_type,
                                        source_node=source_node,
                                        assignment=assignment,
                                        literal_value=literal_value)
        return var_type

    def visit_Global(self, global_node: ast.Global):
        """
        Visitor of the global identifier node

        :param global_node:
        """
        for var_id in global_node.names:
            symbol = self.get_symbol(var_id)
            if isinstance(symbol, Variable):
                if self._current_method is not None:
                    self._current_method.include_variable(var_id, symbol, is_global=True)
                self.__include_variable(var_id, symbol.type, source_node=global_node)

    def visit_Expr(self, expr: ast.Expr):
        """
        Visitor of the atom expression node

        :param expr:
        """
        value = self.visit(expr.value)
        if isinstance(expr.value, ast.Name):
            if (
                    # it is not a symbol of the method scope
                    (self._current_method is not None and value not in self._current_method.symbols)
                    # nor it is a symbol of the module scope
                    or (self._current_module is not None and value not in self._current_module.symbols)
                    # nor it is a symbol of the global scope
                    or value not in self.symbols
            ):
                self._log_error(
                    CompilerError.UnresolvedReference(expr.value.lineno, expr.value.col_offset, value)
                )

    def visit_Subscript(self, subscript: ast.Subscript) -> Union[str, IType]:
        """
        Verifies if it is the types in the subscription are valid

        :param subscript: the python ast subscription node
        :return: if the subscript is not a symbol, returns its type. Otherwise returns the symbol id.
        :rtype: IType or str
        """
        is_internal = hasattr(subscript, 'is_internal_call') and subscript.is_internal_call
        value = self.visit(subscript.value)
        symbol = self.get_symbol(value, is_internal=is_internal, origin_node=subscript.value) if isinstance(value, str) else value

        if isinstance(subscript.ctx, ast.Load):
            if (isinstance(symbol, (Collection, MetaType))
                    and isinstance(subscript.value, (ast.Name, ast.NameConstant, ast.Attribute))):
                # for evaluating names like List[str], Dict[int, bool], etc
                value = subscript.slice.value if isinstance(subscript.slice, ast.Index) else subscript.slice
                values_type: Iterable[IType] = self.get_values_type(value)
                if isinstance(symbol, Collection):
                    return symbol.build_collection(*values_type)
                else:
                    return symbol.build(*values_type)

            symbol_type = self.get_type(symbol)
            if isinstance(subscript.slice, ast.Slice):
                return symbol_type

            if isinstance(symbol, UnionType) or isinstance(symbol_type, UnionType):
                if not isinstance(symbol_type, UnionType):
                    symbol_type = symbol
                index = subscript.slice.value if isinstance(subscript.slice, ast.Index) else subscript.slice
                if isinstance(index, ast.Tuple):
                    union_types = [self.get_type(value) for value in index.elts]
                else:
                    union_types = self.get_type(index)
                return symbol_type.build(union_types)

            if isinstance(symbol_type, Collection):
                return symbol_type.item_type

        return value

    def get_values_type(self, value: ast.AST) -> Iterable[Optional[IType]]:
        """
        Verifies if it is a multiple assignments statement

        :param value: the python ast subscription node
        """
        value_type: Optional[IType] = None

        if isinstance(value, (ast.Subscript, ast.Attribute, ast.Tuple)):
            # index is another subscription
            value_type = self.visit(value)
        elif isinstance(value, ast.Name):
            # index is an identifier
            value_type = self.get_symbol(value.id)

        types: Iterable[Optional[IType]] = value_type if isinstance(value_type, Iterable) else [value_type]
        for tpe in types:
            if not isinstance(tpe, IType):
                # type hint not using identifiers or using identifiers that are not types
                index = self.visit(value)
                if isinstance(index, str):
                    self._log_error(
                        CompilerError.UnresolvedReference(value.lineno, value.col_offset, index)
                    )

        return types

    def visit_Call(self, call: ast.Call) -> Optional[IType]:
        """
        Visitor of a function call node

        :param call: the python ast function call node
        :return: the result type of the called function. None if the function is not found
        """
        func_id = self.visit(call.func)
        func_symbol = self.get_symbol(func_id)

        # if func_symbol is None, the called function may be a function written after in the code
        # that's why it shouldn't log a compiler error here
        if func_symbol is None:
            return None

        if not isinstance(func_symbol, Callable):
            # verify if it is a builtin method with its name shadowed
            func = Builtin.get_symbol(func_id)
            func_symbol = func if func is not None else func_symbol

            if func_symbol is Type.exception:
                func_symbol = Builtin.Exception
            elif isinstance(func_symbol, ClassType):
                func_symbol = func_symbol.constructor_method()

        if not isinstance(func_symbol, Callable):
            # the symbol doesn't exist
            self._log_error(
                CompilerError.UnresolvedReference(call.func.lineno, call.func.col_offset, func_id)
            )
        elif isinstance(func_symbol, IBuiltinMethod):
            if func_symbol.body is not None:
                self._builtin_functions_to_visit[func_id] = func_symbol
            elif func_symbol is Builtin.NewEvent:
                new_event = self.create_new_event(call)
                self.__include_callable(new_event.identifier, new_event)
                self._current_event = new_event
            else:
                args_types = [self.get_type(arg, use_metatype=True) for arg in call.args]
                updated_symbol = func_symbol.build(args_types)

                if updated_symbol.identifier != func_id:
                    self.__include_callable(updated_symbol.identifier, updated_symbol)
                    return self.get_type(updated_symbol)

        return self.get_type(call.func)

    def create_new_event(self, create_call: ast.Call) -> Event:
        event_args = create_call.args
        args = {}
        name = Builtin.Event.identifier

        if len(event_args) < 0:
            self._log_error(
                CompilerError.UnfilledArgument(line=create_call.lineno,
                                               col=create_call.col_offset,
                                               param=list(Builtin.NewEvent.args)[0])
            )
        elif len(event_args) > 0:
            args_type = self.get_type(event_args[0])
            if not Type.list.is_type_of(args_type):
                self._log_error(
                    CompilerError.MismatchedTypes(line=event_args[0].lineno,
                                                  col=event_args[0].col_offset,
                                                  expected_type_id=Type.list.identifier,
                                                  actual_type_id=args_type.identifier)
                )
            else:
                for value in event_args[0].elts:
                    if not isinstance(value, ast.Tuple):
                        CompilerError.MismatchedTypes(line=value.lineno,
                                                      col=value.col_offset,
                                                      expected_type_id=Type.tuple.identifier,
                                                      actual_type_id=self.get_type(value).identifier)
                    elif len(value.elts) < 2:
                        self._log_error(
                            CompilerError.UnfilledArgument(line=value.lineno,
                                                           col=value.col_offset,
                                                           param=list(Builtin.NewEvent.args)[0])
                        )
                    else:
                        event_arg_name, event_arg_type = value.elts
                        are_types_valid = True
                        if not isinstance(event_arg_name, ast.Str):
                            are_types_valid = False
                        else:
                            if isinstance(event_arg_type, ast.Name):  # if is name, get the type of its id
                                arg_type = self.get_symbol(event_arg_type.id)
                            else:  # otherwise, if the result is a type
                                arg_type = self.visit(event_arg_type)

                            from boa3.internal.neo.vm.type.AbiType import AbiType
                            if not isinstance(arg_type, IType):
                                are_types_valid = False
                            elif arg_type.abi_type is AbiType.InteropInterface:
                                self._log_error(
                                    CompilerError.MismatchedTypes(line=event_arg_type.lineno,
                                                                  col=event_arg_type.col_offset,
                                                                  expected_type_id=MetaType.build().identifier,
                                                                  actual_type_id=arg_type.identifier)
                                )

                        if not are_types_valid:
                            self._log_error(
                                CompilerError.MismatchedTypes(line=value.lineno,
                                                              col=value.col_offset,
                                                              expected_type_id=Type.tuple.identifier,
                                                              actual_type_id=self.get_type(value).identifier)
                            )
                        else:
                            arg_name = event_arg_name.s
                            arg_type = (self.get_symbol(event_arg_type.id)
                                        if isinstance(event_arg_type, ast.Name)
                                        else self.visit(event_arg_type))
                            args[arg_name] = Variable(arg_type)

            if len(event_args) > 1:
                if not isinstance(event_args[1], ast.Str):
                    name_type = self.get_type(event_args[1])
                    self._log_error(
                        CompilerError.MismatchedTypes(line=event_args[1].lineno,
                                                      col=event_args[1].col_offset,
                                                      expected_type_id=Type.str.identifier,
                                                      actual_type_id=name_type.identifier)
                    )
                else:
                    name = event_args[1].s

        event = Event(name, args)
        event._origin_node = create_call
        return event

    def visit_Attribute(self, attribute: ast.Attribute) -> Union[ISymbol, str]:
        """
        Gets the attribute inside the ast node

        :param attribute: the python ast attribute node
        :return: returns the type of the value, the attribute symbol and its id if the attribute exists.
                 Otherwise, returns None
        """
        value_id = attribute.value.id if isinstance(attribute.value, ast.Name) else None
        value: ISymbol = self.get_symbol(value_id) if value_id is not None else self.visit(attribute.value)

        if isinstance(value, Variable):
            value = value.type
        if hasattr(value, 'symbols') and attribute.attr in value.symbols:
            return value.symbols[attribute.attr]
        elif isinstance(value, Package) and attribute.attr in value.inner_packages:
            return value.inner_packages[attribute.attr]
        elif Builtin.get_symbol(attribute.attr) is not None:
            return Builtin.get_symbol(attribute.attr)
        elif isinstance(value, UndefinedType):
            return value
        else:
            return '{0}.{1}'.format(value_id, attribute.attr)

    def visit_For(self, for_node: ast.For):
        """
        Visitor of for statement node

        :param for_node: the python ast for node
        """
        iter_type = self.get_type(for_node.iter)
        targets = self.visit(for_node.target)
        iterator_type = iter_type.value_type if hasattr(iter_type, 'value_type') else iter_type

        if isinstance(targets, str):
            self.__include_variable(targets, iterator_type, source_node=for_node.target)
        elif isinstance(iter_type, SequenceType):
            for target in targets:
                if isinstance(target, str):
                    self.__include_variable(target, iterator_type, source_node=for_node.target)

        # continue to walk through the tree
        self.generic_visit(for_node)

    def visit_Match(self, match_node: ast.Match):
        for case in match_node.cases:
            if not (isinstance(case.pattern, (ast.MatchValue, ast.MatchSingleton)) or
                    isinstance(case.pattern, ast.MatchAs) and case.pattern.pattern is None and case.guard is None
            ):
                self._log_error(
                    CompilerError.NotSupportedOperation(
                        case.pattern.lineno, case.pattern.col_offset,
                        symbol_id='case pattern with guard'
                    )
                )
        return super().generic_visit(match_node)

    def visit_ListComp(self, node: ast.ListComp):
        return self._visit_comprehension(node)

    def visit_SetComp(self, node: ast.SetComp):
        return self._visit_comprehension(node)

    def visit_DictComp(self, node: ast.DictComp):
        return self._visit_comprehension(node)

    def _visit_comprehension(self, node):
        # TODO: refactor when comprehension is implemented #2ewev7w #8678dw2ak
        self._log_error(
            CompilerError.NotSupportedOperation(
                node.lineno, node.col_offset,
                symbol_id='list comprehension'
            )
        )
        self.generic_visit(node)
        return node

    def visit_Name(self, name: ast.Name) -> str:
        """
        Visitor of a name node

        :param name:
        :return: the identifier of the name
        """
        return name.id

    def visit_Starred(self, node: ast.Starred):
        # TODO: refactor when starred variables are implemented #2kq1hzg
        self._log_error(
            CompilerError.NotSupportedOperation(
                node.lineno, node.col_offset,
                symbol_id='* variables'
            )
        )
        return node.value

    def visit_Constant(self, constant: ast.Constant) -> Any:
        """
        Visitor of constant values node

        :param constant: the python ast constant value node
        :return: the value of the constant
        """
        return constant.value

    def visit_NameConstant(self, constant: ast.NameConstant) -> Any:
        """
        Visitor of constant names node

        :param constant:
        :return: the value of the constant
        """
        return constant.value

    def visit_Num(self, num: ast.Num) -> int:
        """
        Visitor of literal number node

        :param num:
        :return: the value of the number
        """
        return num.n

    def visit_Str(self, str: ast.Str) -> str:
        """
        Visitor of literal string node

        :param str:
        :return: the value of the string
        """
        return str.s

    def visit_JoinedStr(self, joined_str: ast.JoinedStr):
        """
        Visitor of joined string node

        :param joined_str:
        :return: the value of the string

        """
        for node in joined_str.values:
            self.visit(node)

    def visit_Bytes(self, btes: ast.Bytes) -> bytes:
        """
        Visitor of literal string node

        :param btes:
        :return: the value of the string
        """
        return btes.s

    def visit_Tuple(self, tup_node: ast.Tuple) -> Optional[Tuple[Any, ...]]:
        """
        Visitor of literal tuple node

        :param tup_node: the python ast string node
        :return: the value of the tuple
        """
        result = [self.get_type(value) for value in tup_node.elts]
        if Type.none in result and isinstance(tup_node.ctx, ast.Load):
            # if can't define the type of any value, let it to be defined in the type checking
            # only in load ctx because on store ctx means a tuple of variables to be assigned
            return None
        return tuple(result)

    def visit_List(self, list_node: ast.List) -> Optional[List[Any]]:
        """
        Visitor of literal list node

        :param list_node: the python ast list node
        :return: the value of the list
        """
        result = [self.get_type(value) for value in list_node.elts]
        if Type.none in result:
            # if can't define the type of any value, let it to be defined in the type checking
            return None
        return result

    def visit_Dict(self, dict_node: ast.Dict) -> Optional[Dict[Any, Any]]:
        """
        Visitor of literal dict node

        :param dict_node: the python ast dict node
        :return: the value of the dict
        """
        dictionary = {}
        size = min(len(dict_node.keys), len(dict_node.values))
        for index in range(size):
            key = self.get_type(dict_node.keys[index])
            value = self.get_type(dict_node.values[index])
            if key in dictionary and dictionary[key] != value:
                dictionary[key] = Type.get_generic_type(dictionary[key], value)
            else:
                dictionary[key] = value

        keys = set(dictionary.keys())
        values = set(dictionary.values())

        if Type.none in keys or Type.none in values:
            # if can't define the type of any key or value, let it to be defined in the type checking
            return None
        return dictionary

    def visit_Delete(self, node: ast.Delete) -> Any:
        """
        Visitor of delete statement node. Currently, it's not supported
        """
        self._log_error(
            CompilerError.NotSupportedOperation(
                node.lineno, node.col_offset,
                symbol_id='del keyword'
            )
        )
        self.generic_visit(node)
        return node

    # endregion
