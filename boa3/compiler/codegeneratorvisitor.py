import ast
from typing import Dict, Tuple

from boa3.compiler.codegenerator import CodeGenerator
from boa3.model.method import Method
from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.binaryop import BinaryOp
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

    def store_variable(self, var_id: str, value: ast.AST, index: ast.AST = None):
        # if the value is None, it is a variable declaration
        if value is not None:
            if index is None:
                # if index is None, then it is a variable assignment
                self.visit_to_generate(value)
                self.generator.convert_store_variable(var_id)
            else:
                # if not, it is an array assignment
                self.generator.convert_load_symbol(var_id)
                self.visit_to_generate(index)
                self.visit_to_generate(value)
                self.generator.convert_set_array_item()

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
        var_index = None
        var_id = self.visit(assign.targets[0])

        # if it is a tuple, then it is an array assignment
        if isinstance(var_id, tuple):
            var_index = var_id[1]
            var_id: str = var_id[0]

        self.store_variable(var_id, assign.value, var_index)

    def visit_Subscript(self, subscript: ast.Subscript):
        """
        Visitor of a subscript node

        :param subscript: the python ast subscript node
        """
        if isinstance(subscript.ctx, ast.Load):
            # get item
            self.visit_to_generate(subscript.value)
            self.visit_to_generate(subscript.slice.value)
            self.generator.convert_get_array_item()
        else:
            # set item
            var_id = self.visit(subscript.value)
            return var_id, subscript.slice.value

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
        converted: bool = False
        left = compare.left
        for index, op in enumerate(compare.ops):
            right = compare.comparators[index]
            if isinstance(op, BinaryOperation):
                self.visit_to_generate(left)
                self.visit_to_generate(right)
                self.generator.convert_operation(op)
                # if it's more than two comparators, must include AND between the operations
                if not converted:
                    converted = True
                else:
                    self.generator.convert_operation(BinaryOp.And)
            left = right

    def visit_BoolOp(self, bool_op: ast.BoolOp):
        """
        Visitor of a compare operation node

        :param bool_op: the python ast boolean operation node
        """
        if isinstance(bool_op.op, BinaryOperation):
            left = bool_op.values[0]
            self.visit_to_generate(left)
            for index, right in enumerate(bool_op.values[1:]):
                self.visit_to_generate(right)
                self.generator.convert_operation(bool_op.op)

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

    def visit_If(self, if_node: ast.If):
        """
        Verifies if the type of if test is valid

        :param if_node: the python ast if statement node
        """
        self.visit_to_generate(if_node.test)

        start_addr: int = self.generator.convert_begin_if()
        for stmt in if_node.body:
            self.visit_to_generate(stmt)

        if len(if_node.orelse) > 0:
            start_addr = self.generator.convert_begin_else(start_addr)
            for stmt in if_node.orelse:
                self.visit_to_generate(stmt)

        self.generator.convert_end_if(start_addr)

    def visit_IfExp(self, if_node: ast.IfExp):
        """
        Verifies if the type of if test is valid

        :param if_node: the python ast if statement node
        """
        self.visit_to_generate(if_node.test)

        start_addr: int = self.generator.convert_begin_if()
        self.visit_to_generate(if_node.body)

        start_addr = self.generator.convert_begin_else(start_addr)
        self.visit_to_generate(if_node.orelse)

        self.generator.convert_end_if(start_addr)

    def visit_Call(self, call: ast.Call):
        """
        Visitor of a function call node

        :param call: the python ast function call node
        """
        # the parameters are included into the stack in the reversed order
        for arg in reversed(call.args):
            self.visit_to_generate(arg)
        function_id = self.visit(call.func)
        self.generator.convert_load_symbol(function_id)

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

    def visit_Tuple(self, tup_node: ast.Tuple):
        """
        Visitor of literal tuple node

        :param tup_node: the python ast string node
        :return: the value of the tuple
        """
        tup = tuple([value for value in tup_node.elts])
        length = len(tup_node.elts)
        self.generator.convert_new_array(length)
        for index, value in enumerate(tup_node.elts):
            self.generator.convert_set_new_array_item_at(index)
            self.visit_to_generate(value)
            self.generator.convert_set_array_item()
