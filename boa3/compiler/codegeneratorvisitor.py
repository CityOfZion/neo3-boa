import ast
from typing import Tuple, Dict, Any

from boa3.compiler.codegenerator import CodeGenerator
from boa3.model.method import Method
from boa3.model.symbol import ISymbol
from boa3.model.type.type import IType
from boa3.model.variable import Variable


class VisitorCodeGenerator(ast.NodeVisitor):
    """
    This class is responsible for walk through the ast.

    :ivar generator:
    """

    def __init__(self, generator: CodeGenerator):
        self.generator = generator

    def visit_FunctionDef(self, function: ast.FunctionDef):
        """
        Visitor of the function definition node

        Generates the Neo VM code for the function

        :param function: the python ast function definition node
        """
        fun_args: Dict[str, Variable] = self.visit(function.args)
        if function.returns is not None:
            fun_rtype_id: str = self.visit(function.returns)
        else:
            fun_rtype_id: str = 'None'

        symbol: ISymbol = self.generator.get_symbol(fun_rtype_id)
        if isinstance(symbol, IType):
            fun_return: IType = symbol
            method = Method(fun_args, fun_return)
            self.generator.convert_begin_method(method)

            for stmt in function.body:
                self.visit(stmt)
            self.generator.convert_end_method()

    def visit_arguments(self, arguments: ast.arguments) -> Dict[str, Variable]:
        """
        Visitor of the function arguments node

        :param arguments: the python ast function arguments node
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

        :param arg: the python ast arg node
        :return: a tuple with the identifier and the argument
        """
        var_id = arg.arg
        var_type = self.visit(arg.annotation)

        return var_id, Variable(var_type)

    def visit_Return(self, ret: ast.Return):
        """
        Visitor of a function return node

        :param ret: the python ast return node
        """
        if ret.value is not None:
            value = self.visit(ret.value)
            if ret.value is not ast.Name:
                self.generator.convert_literal(value)
            else:
                # TODO: validate variables and function calls
                pass

    def visit_Name(self, name: ast.Name) -> str:
        """
        Visitor of a name node

        :param name: the python ast name identifier node
        :return: the identifier of the name
        """
        return name.id

    def visit_NameConstant(self, constant: ast.NameConstant) -> Any:
        """
        Visitor of constant names node

        :param constant: the python ast name constant node
        :return: the value of the constant
        """
        return constant.value

    def visit_Num(self, num: ast.Num) -> int:
        """
        Visitor of literal number node

        :param num: the python ast number node
        :return: the value of the number
        """
        return num.n

    def visit_Str(self, str: ast.Str):
        """
        Visitor of literal string node

        :param str: the python ast string node
        :return: the value of the string
        """
        return str.s
