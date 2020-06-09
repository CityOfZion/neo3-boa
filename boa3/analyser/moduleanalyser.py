import ast
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from boa3 import helpers
from boa3.analyser.astanalyser import IAstAnalyser
from boa3.exception import CompilerError, CompilerWarning
from boa3.model.builtin.builtin import Builtin
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.method import Method
from boa3.model.module import Module
from boa3.model.symbol import ISymbol
from boa3.model.type.itype import IType
from boa3.model.type.sequence.sequencetype import SequenceType
from boa3.model.type.type import Type
from boa3.model.variable import Variable


class ModuleAnalyser(IAstAnalyser, ast.NodeVisitor):
    """
    This class is responsible for mapping the locals of the functions and modules

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.

    :ivar modules: a dictionary that maps each module with its name. Empty by default.
    :ivar symbols: a dictionary that maps the global symbols.
    """

    def __init__(self, ast_tree: ast.AST, symbol_table: Dict[str, ISymbol]):
        super().__init__(ast_tree)
        self.modules: Dict[str, Module] = {}
        self.symbols: Dict[str, ISymbol] = symbol_table

        self.__builtin_functions_to_visit: Dict[str, IBuiltinMethod] = {}
        self.__current_module: Module = None
        self.__current_method: Method = None

        self.visit(self._tree)

    @property
    def __current_scope(self):
        """
        Returns the scope that is currently being analysed

        :return: the current scope. Return None if it is the global scope
        :rtype: Method or Module or None
        """
        if self.__current_method is not None:
            return self.__current_method
        return self.__current_module

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

    def __include_variable(self, var_id: str, var_type_id: Union[str, IType], source_node: ast.AST, var_enumerate_type: IType = Type.none):
        """
        Includes the variable in the symbol table if the id was not used

        :param var_id: variable id
        :param var_type_id: variable type id
        :type var_type_id: str or IType
        :param var_enumerate_type: variable value type id if var_type_id is a SequenceType
        """
        if var_id not in self.__current_scope.symbols:
            outer_symbol = self.get_symbol(var_id)
            if outer_symbol is not None:
                self._log_warning(
                    CompilerWarning.NameShadowing(source_node.lineno, source_node.col_offset, outer_symbol, var_id)
                )

            var_type = None
            if isinstance(var_type_id, SequenceType):
                var_type = var_type_id
                var_enumerate_type = self.get_enumerate_type(var_type)
            else:
                if isinstance(var_type_id, IType):
                    var_type_id = var_type_id.identifier
                    var_type = self.symbols[var_type_id]

            # when setting a None value to a variable, set the variable as any type
            if var_type is Type.none:
                var_type = Type.any

            if isinstance(var_type, IType) or var_type is None:
                # if type is None, the variable type depends on the type of a expression
                if isinstance(var_type, SequenceType):
                    var_type = var_type.build_sequence(var_enumerate_type)
                var = Variable(var_type)
                self.__current_scope.include_variable(var_id, var)

    def __include_method(self, method_id: str, method: Method):
        """
        Includes the method in the symbol table if the id was not used

        :param method_id: method id
        :param method: method to be included
        """
        if method_id not in self.__current_module.symbols:
            self.__current_module.include_method(method_id, method)

    def get_symbol(self, symbol_id: str) -> Optional[ISymbol]:
        if symbol_id in self.__current_scope.symbols:
            # the symbol exists in the local scope
            return self.__current_scope.symbols[symbol_id]
        elif symbol_id in self.__current_module.symbols:
            # the symbol exists in the module scope
            return self.__current_module.symbols[symbol_id]
        else:
            return super().get_symbol(symbol_id)

    def visit_Module(self, module: ast.Module):
        """
        Visitor of the module node

        Fills module symbol table

        :param module:
        """
        mod: Module = Module()
        self.__current_module = mod
        for stmt in module.body:
            self.visit(stmt)
        # TODO: include the body of the builtin methods to the ast
        # TODO: get module name
        self.modules['main'] = mod
        self.__current_module = None

    def visit_FunctionDef(self, function: ast.FunctionDef):
        """
        Visitor of the function node

        Includes the method in the scope of its module

        :param function:
        """
        fun_args = self.visit(function.args)
        fun_rtype_symbol = self.visit(function.returns) if function.returns is not None else Type.none

        if fun_rtype_symbol is None:
            # it is a function with None return: Main(a: int) -> None:
            raise NotImplementedError

        if isinstance(fun_rtype_symbol, str):
            symbol = self.get_symbol(function.returns.id.lower())
            fun_rtype_symbol = self.get_type(symbol)

        fun_decorators = [self.visit(decorator) for decorator in function.decorator_list]
        fun_return: IType = self.get_type(fun_rtype_symbol)
        method = Method(fun_args, fun_return, Builtin.Public.identifier in fun_decorators)

        if function.name in ['main', 'Main']:
            # don't show return when the function is void
            return_type = ' -> {0}'.format(fun_return.identifier) if fun_return is not Type.none else ''
            arg_types = ', '.join(['{0}: {1}'.format(arg, var.type.identifier) for arg, var in fun_args.items()])

            logging.info("Main method found at {0}:{1}: '{2}({3}){4}'"
                         .format(function.lineno, function.col_offset, function.name, arg_types, return_type))
            # main method is always public
            method.set_as_main_method()

        self.__current_method = method

        for stmt in function.body:
            self.visit(stmt)

        self.__include_method(function.name, method)
        self.__current_method = None

    def visit_arguments(self, arguments: ast.arguments) -> Dict[str, Variable]:
        """
        Visitor of the function arguments node

        :param arguments:
        :return: a dictionary that maps each argument to its identifier
        """
        args: Dict[str, Variable] = {}

        for arg in arguments.args:
            var_id, var = self.visit_arg(arg)   # Tuple[str, Variable]
            args[var_id] = var
        return args

    def visit_arg(self, arg: ast.arg) -> Tuple[str, Variable]:
        """
        Visitor of a function argument node

        :param arg:
        :return: a tuple with the identifier and the argument
        """
        var_id = arg.arg
        var_type: IType = self.get_type(arg.annotation)

        if var_type is Type.none and isinstance(arg.annotation, ast.Name):
            var_symbol: ISymbol = self.get_symbol(arg.annotation.id.lower())
            var_type = self.get_type(var_symbol)

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
                # the symbol doesn't exists
                self._log_error(
                    CompilerError.UnresolvedReference(ret.value.lineno, ret.value.col_offset, symbol_id)
                )

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
                symbol = self.get_symbol(target_type.lower())
            if symbol is None:
                # the symbol doesn't exists
                self._log_error(
                    CompilerError.UnresolvedReference(target.lineno, target.col_offset, target_type)
                )
            target_type = symbol

        if target_type is None and not isinstance(target, ast.NameConstant):
            # the value type is invalid
            return None
        return self.get_type(target_type)

    def get_enumerate_type(self, var_type: IType) -> IType:
        return var_type.value_type if isinstance(var_type, SequenceType) else Type.none

    def visit_Assign(self, assign: ast.Assign):
        """
        Visitor of the variable assignment node

        Includes the variable in its scope if it's the first use

        :param assign:
        """
        var_id = self.visit(assign.targets[0])
        var_type = self.visit_type(assign.value)

        self.__include_variable(var_id, var_type, source_node=assign)

    def visit_AnnAssign(self, ann_assign: ast.AnnAssign):
        """
        Visitor of the annotated variable assignment node

        Includes the variable in its scope if it's the first use

        :param ann_assign:
        """
        var_id: str = self.visit(ann_assign.target)
        var_type: IType = self.visit_type(ann_assign.annotation)

        # TODO: check if the annotated type and the value type are the same
        self.__include_variable(var_id, var_type, source_node=ann_assign)

    def visit_Expr(self, expr: ast.Expr):
        """
        Visitor of the atom expression node

        :param expr:
        """
        value = self.visit(expr.value)
        if isinstance(expr.value, ast.Name):
            if (
                # it is not a symbol of the method scope
                (self.__current_method is not None and value not in self.__current_method.symbols)
                # nor it is a symbol of the module scope
                or (self.__current_module is not None and value not in self.__current_module.symbols)
                # nor it is a symbol of the global scope
                or value not in self.symbols
            ):
                self._log_error(
                    CompilerError.UnresolvedReference(expr.value.lineno, expr.value.col_offset, value)
                )

    def visit_Subscript(self, subscript: ast.Subscript):
        """
        Verifies if it is the types in the subscription are valid

        :param subscript: the python ast subscription node
        :return: if the subscript is not a symbol, returns its type. Otherwise returns the symbol id.
        :rtype: IType or str
        """
        value = self.visit(subscript.value)
        symbol = self.get_symbol(value)

        if symbol is None:
            symbol = self.get_symbol(value.lower())
            subscript.value.id = value.lower() if symbol is not None else subscript.value

        if isinstance(subscript.ctx, ast.Load):
            if isinstance(symbol, SequenceType):
                values_type: IType = self.get_values_type(subscript.slice.value)
                return symbol.build_sequence(values_type)

            symbol_type = self.get_type(symbol)
            if isinstance(symbol_type, SequenceType):
                return symbol_type.value_type

        return value

    def get_values_type(self, value: ast.AST):
        """
        Verifies if it is a multiple assignments statement

        :param value: the python ast subscription node
        """
        value_type: Optional[IType] = None

        if isinstance(value, ast.Subscript):
            # index is another subscription
            value_type = self.visit(value)
        elif isinstance(value, ast.Name):
            # index is an identifier
            value_type = self.get_symbol(value.id)
            if value_type is None:
                value_type = self.get_symbol(value.id.lower())
                value.id = value.id.lower() if value_type is not None else value.id

        if not isinstance(value_type, IType):
            # type hint not using identifiers or using identifiers that are not types
            index = self.visit(value)
            self._log_error(
                CompilerError.UnresolvedReference(value.lineno, value.col_offset, index)
            )

        return value_type

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

        if not isinstance(func_symbol, Method):
            # the symbol doesn't exists
            self._log_error(
                CompilerError.UnresolvedReference(call.func.lineno, call.func.col_offset, func_id)
            )
        elif isinstance(func_symbol, IBuiltinMethod) and func_symbol.body is not None:
            self.__builtin_functions_to_visit[func_id] = func_symbol

        return self.get_type(call.func)

    def visit_For(self, for_node: ast.For):
        """
        Visitor of for statement node

        :param for_node: the python ast for node
        """
        iter_type = self.get_type(for_node.iter)
        targets = self.visit(for_node.target)

        if isinstance(iter_type, SequenceType):
            if isinstance(targets, str):
                self.__include_variable(targets, iter_type.value_type, source_node=for_node.target)
            else:
                for target in targets:
                    if isinstance(target, str):
                        self.__include_variable(target, iter_type.value_type, source_node=for_node.target)

            for_iter_id = helpers.get_auxiliary_name(for_node, 'iter')
            for_index_id = helpers.get_auxiliary_name(for_node, 'index')

            self.__include_variable(for_iter_id, iter_type, source_node=for_node.iter)
            self.__include_variable(for_index_id, iter_type.valid_key, source_node=for_node)

        # continue to walk through the tree
        self.generic_visit(for_node)

    def visit_Name(self, name: ast.Name) -> str:
        """
        Visitor of a name node

        :param name:
        :return: the identifier of the name
        """
        return name.id

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

    def visit_Tuple(self, tup_node: ast.Tuple) -> Tuple[Any, ...]:
        """
        Visitor of literal tuple node

        :param tup_node: the python ast string node
        :return: the value of the tuple
        """
        return tuple([self.get_type(value) for value in tup_node.elts])

    def visit_List(self, list_node: ast.List) -> List[Any]:
        """
        Visitor of literal list node

        :param list_node: the python ast list node
        :return: the value of the list
        """
        return [self.get_type(value) for value in list_node.elts]
