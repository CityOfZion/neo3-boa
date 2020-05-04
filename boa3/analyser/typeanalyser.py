import ast
from ast import NodeVisitor
from typing import List, Dict

from boa3.analyser.astanalyser import IAstAnalyser
from boa3.exception.CompilerError import *
from boa3.model.module import Module


class TypeAnalyser(NodeVisitor, IAstAnalyser):
    """
    This class is responsible for the type checking of the code

    :ivar type_errors: a list with the found type errors. Empty by default.
    """

    def __init__(self, ast_tree: ast.AST):
        super().__init__(ast_tree)
        self.type_errors: List[Exception] = []
        self.modules: Dict[str, Module] = {}

        self.visiting_function_return: Optional[str] = None

        self.visit(self._tree)

    def _log_error(self, error: CompilerError):
        self.errors.append(error)
        raise error

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
        if function.returns is not None:
            if isinstance(function.returns, ast.Name):
                self.visiting_function_return = function.returns.id
            elif isinstance(function.returns, ast.NameConstant):
                self.visiting_function_return = function.returns.value

        for stmt in function.body:
            self.visit(stmt)
        self.visiting_function_return = None

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
                TypeHintMissing(arg.lineno, arg.col_offset, symbol_id=arg.arg)
            )

    def visit_Return(self, ret: ast.Return):
        """
        Verifies if the return of the function is the same type as the return type annotation

        :param ret: the python ast return node
        """
        if ret.value is not None:
            # it is returning something, but there is no type hint for return
            if self.visiting_function_return is None:
                self._log_error(
                    TypeHintMissing(ret.lineno, ret.col_offset, symbol_id=ret.arg)
                )
                return
            # multiple returns are not allowed
            elif isinstance(ret.value, ast.Tuple):
                self._log_error(
                    TooManyReturns(ret.lineno, ret.col_offset)
                )
                return
            # TODO: check if the type of return is the same as in the type hint
        elif self.visiting_function_return is not None:
            # the return is None, but the type hint value type is not None
            self._log_error(
                MismatchedTypes(
                    ret.lineno, ret.col_offset,
                    actual_type_id='None',
                    expected_type_id=self.visiting_function_return)
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
                InvalidType(num.lineno, num.col_offset, symbol_id=type(num.n).__name__)
            )
        return num.n
