import ast
from typing import Dict, Tuple

from boa3.compiler.codegenerator import CodeGenerator
from boa3.model.method import Method
from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.unary.unaryoperation import UnaryOperation
from boa3.model.symbol import ISymbol
from boa3.model.type.itype import IType
from boa3.model.type.type import Type
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

    def visit_to_generate(self, node: ast.AST):
        """
        Visitor to generate the nodes that the primary visitor is used to retrieve value

        :param node: an ast node
        """
        result = self.visit(node)

        # the default return of the name visitor is the name string
        if isinstance(node, ast.Name):
            # TODO: validate function calls
            self.generator.convert_load_symbol(result)

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
            self.visit_to_generate(ret.value)

    def store_variable(self, var_id: str, value: ast.AST):
        # if the value is None, it is a variable declaration
        if value is not None:
            self.visit_to_generate(value)
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

    def visit_BinOp(self, bin_op: ast.BinOp):
        """
        Visitor of a binary operation node

        :param bin_op: the python ast binary operation node
        """
        if isinstance(bin_op.op, BinaryOperation):
            self.visit_to_generate(bin_op.left)
            self.visit_to_generate(bin_op.right)
            self.generator.convert_operation(bin_op.op)

    def visit_UnaryOp(self, un_op: ast.UnaryOp):
        """
        Visitor of a binary operation node

        :param un_op: the python ast binary operation node
        """
        if isinstance(un_op.op, UnaryOperation):
            self.visit_to_generate(un_op.operand)
            self.generator.convert_operation(un_op.op)

    def visit_Compare(self, compare: ast.Compare):
        """
        Visitor of a compare operation node

        :param compare: the python ast compare operation node
        """
        left = compare.left
        for index, op in enumerate(compare.ops):
            right = compare.comparators[index]
            if isinstance(op, BinaryOperation):
                self.visit_to_generate(left)
                self.visit_to_generate(right)
                self.generator.convert_operation(op)
            left = right

    def visit_While(self, while_node: ast.While):
        """
        Verifies if the type of while test is valid

        :param while_node: the python ast while statement node
        """
        start_addr: int = self.generator.convert_begin_while()
        for stmt in while_node.body:
            self.visit_to_generate(stmt)

        test_address: int = self.generator.address
        self.visit_to_generate(while_node.test)
        self.generator.convert_end_while(start_addr, test_address)

        for stmt in while_node.orelse:
            self.visit_to_generate(stmt)

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
        """
        self.generator.convert_literal(num.n)

    def visit_Str(self, str: ast.Str):
        """
        Visitor of literal string node

        :param str: the python ast string node
        """
        self.generator.convert_literal(str.s)
