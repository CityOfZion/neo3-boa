import ast
from typing import Dict, Tuple

from boa3.compiler.codegenerator import CodeGenerator
from boa3.model.method import Method
from boa3.model.symbol import ISymbol
from boa3.model.type.type import Type, IType
from boa3.model.variable import Variable


class VisitorCodeGenerator(ast.NodeVisitor):
    """
    This class is responsible for walk through the ast.

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.

    :ivar generator:
    """

    def __init__(self, generator: CodeGenerator):
        self.generator = generator

    @property
    def symbols(self) -> Dict[str, ISymbol]:
        return self.generator.symbol_table

    def visit_FunctionDef(self, function: ast.FunctionDef):
        """
        Visitor of the function definition node

        Generates the Neo VM code for the function

        :param function: the python ast function definition node
        """
        method = self.symbols[function.name]
        if function.returns is not None:
            fun_rtype_id: str = self.visit(function.returns)
        else:
            fun_rtype_id: str = Type.none.identifier

        symbol: ISymbol = self.generator.get_symbol(fun_rtype_id)
        if isinstance(method, Method) and isinstance(symbol, IType):
            fun_return: IType = symbol
            method.return_type = fun_return

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
            if ret.value is not ast.Name and value is not None:
                self.generator.convert_literal(value)
            else:
                # TODO: validate variables and function calls
                pass

    def store_variable(self, var_id: str, value: ast.AST):
        # if the value is None, it is a variable declaration
        if value is not None:
            if isinstance(value, ast.Name):
                value_id: str = self.visit(value)
                var_value = self.symbols[var_id]
                # TODO: implement conversion of variable and function calls
            else:
                # visit to convert the expression of the assignment
                self.visit(value)

            self.generator.convert_store_variable(var_id)

    def visit_AnnAssign(self, ann_assign: ast.AnnAssign):
        """
        Visitor of an annotated assignment node

        :param ann_assign: the python ast variable assignment node
        """
        var_id = self.visit(ann_assign.target)
        self.store_variable(var_id, ann_assign.value)

    def visit_Assign(self, assign: ast.Assign):
        """
        Visitor of an assignment node

        :param assign: the python ast variable assignment node
        """
        var_id = self.visit(assign.targets[0])
        self.store_variable(var_id, assign.value)

    def visit_Name(self, name: ast.Name) -> str:
        """
        Visitor of a name node

        :param name: the python ast name identifier node
        :return: the identifier of the name
        """
        return name.id

    def visit_NameConstant(self, constant: ast.NameConstant):
        """
        Visitor of constant names node

        :param constant: the python ast name constant node
        :return: the value of the constant
        """
        self.generator.convert_literal(constant.value)

    def visit_Num(self, num: ast.Num):
        """
        Visitor of literal number node

        :param num: the python ast number node
        :return: the value of the number
        """
        self.generator.convert_literal(num.n)

    def visit_Str(self, str: ast.Str):
        """
        Visitor of literal string node

        :param str: the python ast string node
        :return: the value of the string
        """
        self.generator.convert_literal(str.s)
