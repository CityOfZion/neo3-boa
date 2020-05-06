import ast
from typing import Dict, Tuple, Any, Optional

from boa3.analyser.astanalyser import IAstAnalyser
from boa3.exception import CompilerError
from boa3.exception.CompilerError import CompilerError as Error
from boa3.model.method import Method
from boa3.model.module import Module
from boa3.model.symbol import ISymbol
from boa3.model.type.type import IType
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

        self.__current_module: Module = None
        self.__current_method: Method = None

        self.visit(self._tree)

    def _log_error(self, error: Error):
        self.errors.append(error)
        raise error

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

    def __include_variable(self, var_id: str, var_type_id: str):
        """
        Includes the variable in the symbol table if the id was not used

        :param var_id: variable id
        :param var_type_id: variable type id
        """
        if var_id not in self.__current_scope.symbols:
            var_type: ISymbol = self.symbols[var_type_id]

            if isinstance(var_type, IType):
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
        elif symbol_id in self.symbols:
            # the symbol exists in the global scope
            return self.symbols[symbol_id]
        else:
            return None

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
        fun_rtype_symbol = self.get_type(function.returns)

        fun_return: IType = fun_rtype_symbol
        method = Method(fun_args, fun_return)
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

    def visit_Assign(self, assign: ast.Assign):
        """
        Visitor of the variable assignment node

        Includes the variable in its scope if it's the first use

        :param assign:
        """
        var_id = self.visit(assign.targets[0])
        var_value = self.visit(assign.value)
        if isinstance(assign.value, ast.Name):
            symbol = self.get_symbol(var_value)
            if symbol is None:
                # the symbol doesn't exists
                self._log_error(
                    CompilerError.UnresolvedReference(assign.value.lineno, assign.value.col_offset, var_value)
                )
            var_type_id = self.get_type(symbol).identifier
        else:
            var_type_id = self.get_type(var_value).identifier

        self.__include_variable(var_id, var_type_id)

    def visit_AnnAssign(self, ann_assign: ast.AnnAssign):
        """
        Visitor of the annotated variable assignment node

        Includes the variable in its scope if it's the first use

        :param ann_assign:
        """
        var_id: str = self.visit(ann_assign.target)
        var_type_id: str = self.visit(ann_assign.annotation)
        self.__include_variable(var_id, var_type_id)

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
