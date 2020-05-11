import ast
from typing import List, Dict

from boa3.analyser.astanalyser import IAstAnalyser
from boa3.exception import CompilerError
from boa3.exception.CompilerError import CompilerError as Error
from boa3.model.method import Method
from boa3.model.module import Module
from boa3.model.symbol import ISymbol
from boa3.model.type.type import Type


class TypeAnalyser(IAstAnalyser, ast.NodeVisitor):
    """
    This class is responsible for the type checking of the code

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.

    :ivar type_errors: a list with the found type errors. Empty by default.
    :ivar modules: a list with the analysed modules. Empty by default.
    :ivar symbols: a dictionary that maps the global symbols.
    """

    def __init__(self, ast_tree: ast.AST, symbol_table: Dict[str, ISymbol]):
        super().__init__(ast_tree)
        self.type_errors: List[Exception] = []
        self.modules: Dict[str, Module] = {}
        self.symbols: Dict[str, ISymbol] = symbol_table

        self.__current_method: Method = None

        self.visit(self._tree)

    def _log_error(self, error: Error):
        self.errors.append(error)
        raise error

    @property
    def __current_method_id(self) -> str:
        """
        Get the string identifier of the current method

        :return: The name identifier of the method. If the current method is None, returns None.
        :rtype: str or None
        """
        if self.__current_method in self.symbols.values():
            index = list(self.symbols.values()).index(self.__current_method)
            return list(self.symbols.keys())[index]

    def visit_Module(self, module: ast.Module):
        """
        Visitor of the module node

        Performs the type checking in the body of the method

        :param module: the python ast module node
        """
        for stmt in module.body:
            self.visit(stmt)

    def visit_FunctionDef(self, function: ast.FunctionDef):
        """
        Visitor of the function node

        Performs the type checking in the body of the function

        :param function: the python ast function definition node
        """
        self.visit(function.args)
        method = self.symbols[function.name]
        self.__current_method = method

        for stmt in function.body:
            self.visit(stmt)
        self.__current_method = None

    def visit_arguments(self, arguments: ast.arguments):
        """
        Verifies if each argument of a function has a type annotation

        :param arguments: the python ast function arguments node
        """
        for arg in arguments.args:
            self.visit(arg)

    def visit_arg(self, arg: ast.arg):
        """
        Verifies if the argument of a function has a type annotation

        :param arg: the python ast arg node
        """
        if arg.annotation is None:
            self._log_error(
                CompilerError.TypeHintMissing(arg.lineno, arg.col_offset, symbol_id=arg.arg)
            )

    def visit_Return(self, ret: ast.Return):
        """
        Verifies if the return of the function is the same type as the return type annotation

        :param ret: the python ast return node
        """
        if ret.value is not None:
            # multiple returns are not allowed
            if isinstance(ret.value, ast.Tuple):
                self._log_error(
                    CompilerError.TooManyReturns(ret.lineno, ret.col_offset)
                )
                return
            # it is returning something, but there is no type hint for return
            elif self.__current_method.return_type is Type.none:
                self._log_error(
                    CompilerError.TypeHintMissing(ret.lineno, ret.col_offset, symbol_id=self.__current_method_id)
                )
                return
            # TODO: check if the type of return is the same as in the type hint
        elif self.__current_method.return_type is not Type.none:
            # the return is None, but the type hint value type is not None
            self._log_error(
                CompilerError.MismatchedTypes(
                    ret.lineno, ret.col_offset,
                    actual_type_id=Type.none.identifier,
                    expected_type_id=self.__current_method.return_type.identifier)
            )

    def visit_Assign(self, assign: ast.Assign):
        """
        Verifies if it is a multiple assignments statement

        :param assign: the python ast variable assignment node
        """
        # multiple assignments
        if len(assign.targets) > 1:
            self._log_error(
                CompilerError.NotSupportedOperation(assign.lineno, assign.col_offset, 'Multiple variable assignments')
            )

        # multiple assignments with tuples
        if isinstance(assign.targets[0], ast.Tuple):
            self._log_error(
                CompilerError.NotSupportedOperation(assign.lineno, assign.col_offset, 'Multiple variable assignments')
            )

    def visit_Num(self, num: ast.Num) -> int:
        """
        Verifies if the number is an integer

        :param num: the python ast number node
        :return: returns the value of the number
        """
        if not isinstance(num.n, int):
            # only integer numbers are allowed
            self._log_error(
                CompilerError.InvalidType(num.lineno, num.col_offset, symbol_id=type(num.n).__name__)
            )
        return num.n
