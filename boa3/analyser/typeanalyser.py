import ast
from typing import List, Dict, Optional, Any

from boa3.analyser.astanalyser import IAstAnalyser
from boa3.exception import CompilerError
from boa3.exception.CompilerError import CompilerError as Error
from boa3.model.method import Method
from boa3.model.module import Module
from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.binaryop import BinaryOp
from boa3.model.operation.operator import Operator
from boa3.model.operation.unary.unaryoperation import UnaryOperation
from boa3.model.operation.unaryop import UnaryOp
from boa3.model.symbol import ISymbol
from boa3.model.type.type import Type, IType


class TypeAnalyser(IAstAnalyser, ast.NodeVisitor):
    """
    This class is responsible for the type checking of the code

    The methods with the name starting with 'visit_' are implementations of methods from the :class:`NodeVisitor` class.
    These methods are used to walk through the Python abstract syntax tree.

    :ivar type_errors: a list with the found type errors. Empty by default.
    :ivar modules: a list with the analysed modules. Empty by default.
    :ivar symbols: a dictionary that maps the global symbols.
    :cvar __operators: a dictionary that maps each operator from Python ast to its equivalent Boa operator.
    """

    def __init__(self, ast_tree: ast.AST, symbol_table: Dict[str, ISymbol]):
        super().__init__(ast_tree)
        self.type_errors: List[Exception] = []
        self.modules: Dict[str, Module] = {}
        self.symbols: Dict[str, ISymbol] = symbol_table

        self.__current_method: Method = None

        self.visit(self._tree)

    __operators = {
        ast.Add: Operator.Plus,
        ast.Sub: Operator.Minus,
        ast.Mult: Operator.Mult,
        ast.FloorDiv: Operator.IntDiv,
        ast.Mod: Operator.Mod,
        ast.UAdd: Operator.Plus,
        ast.USub: Operator.Minus,
        ast.Eq: Operator.Eq,
        ast.NotEq: Operator.NotEq,
        ast.Lt: Operator.Lt,
        ast.LtE: Operator.LtE,
        ast.Gt: Operator.Gt,
        ast.GtE: Operator.GtE,
        ast.Is: Operator.Is,
        ast.IsNot: Operator.IsNot
    }

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

    @property
    def __modules_symbols(self) -> Dict[str, ISymbol]:
        """
        Gets all the symbols in the modules scopes.

        :return: Returns a dictionary that maps the modules symbols.
        """
        symbols = {}
        for module in self.modules.values():
            symbols.update(module.symbols)
        return symbols

    def get_symbol(self, symbol_id: str) -> Optional[ISymbol]:
        if self.__current_method is not None and symbol_id in self.__current_method.symbols:
            # the symbol exists in the local scope
            return self.__current_method.symbols[symbol_id]
        elif symbol_id in self.modules:
            # the symbol exists in the modules scope
            return self.modules[symbol_id]
        elif symbol_id in self.symbols:
            # the symbol exists in the global scope
            return self.symbols[symbol_id]
        else:
            # the symbol was not found
            return None

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

        # continue to walk through the tree
        self.generic_visit(arguments)

    def visit_arg(self, arg: ast.arg):
        """
        Verifies if the argument of a function has a type annotation

        :param arg: the python ast arg node
        """
        if arg.annotation is None:
            self._log_error(
                CompilerError.TypeHintMissing(arg.lineno, arg.col_offset, symbol_id=arg.arg)
            )

        # continue to walk through the tree
        self.generic_visit(arg)

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

        # continue to walk through the tree
        self.generic_visit(ret)

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

        # continue to walk through the tree
        self.generic_visit(assign)

    def visit_While(self, while_node: ast.While):
        """
        Verifies if the type of while test is valid

        :param while_node: the python ast while statement node
        """
        test = self.visit(while_node.test)
        test_type: IType = self.get_type(test)

        if test_type is not Type.bool:
            self._log_error(
                CompilerError.MismatchedTypes(
                    while_node.lineno, while_node.col_offset,
                    actual_type_id=test_type.identifier,
                    expected_type_id=Type.bool.identifier)
            )

        # continue to walk through the tree
        for stmt in while_node.body:
            self.visit(stmt)
        for stmt in while_node.orelse:
            self.visit(stmt)

    def visit_BinOp(self, bin_op: ast.BinOp) -> Optional[IType]:
        """
        Verifies if the types of the operands are valid to the operation

        If the operation is valid, changes de Python operator by the Boa operator in the syntax tree

        :param bin_op: the python ast binary operation node
        :return: the type of the result of the operation if the operation is valid. Otherwise, returns None
        :rtype: IType or None
        """
        operator: Operator = self.get_operator(bin_op.op)
        r_operand = self.visit(bin_op.right)
        l_operand = self.visit(bin_op.left)

        if not isinstance(operator, Operator):
            # the operator is invalid or it was not implemented yet
            self._log_error(
                CompilerError.UnresolvedReference(bin_op.lineno, bin_op.col_offset, type(bin_op.op).__name__)
            )

        try:
            operation: BinaryOperation = self.get_bin_op(operator, r_operand, l_operand)
            if operation is None:
                self._log_error(
                    CompilerError.NotSupportedOperation(bin_op.lineno, bin_op.col_offset, operator)
                )
            elif not operation.is_supported:
                # TODO: concat and power not implemented yet
                # number float division is not supported by Neo VM
                self._log_error(
                    CompilerError.NotSupportedOperation(bin_op.lineno, bin_op.col_offset, operator)
                )
            else:
                bin_op.op = operation
                return operation.result
        except CompilerError.MismatchedTypes as raised_error:
            expected_types = raised_error.args[2]
            actual_types = raised_error.args[3]
            self._log_error(
                CompilerError.MismatchedTypes(bin_op.lineno, bin_op.col_offset, expected_types, actual_types)
            )

    def get_bin_op(self, operator: Operator, right: Any, left: Any) -> BinaryOperation:
        """
        Returns the binary operation specified by the operator and the types of the operands

        :param operator: the operator
        :param right: right operand
        :param left: left operand

        :return: Returns the corresponding :class:`BinaryOperation` if the types are valid.
        :raise MismatchedTypes: raised if the types aren't valid for the operator
        """
        l_type: IType = self.get_type(left)
        r_type: IType = self.get_type(right)

        actual_types: str = "%s', '%s" % (l_type.identifier, r_type.identifier)
        operation: BinaryOperation = BinaryOp.validate_type(operator, l_type, r_type)

        if operation is not None:
            return operation
        else:
            expected_op: BinaryOperation = BinaryOp.get_operation_by_operator(operator)
            expected_types: str = "%s', '%s" % (expected_op.left_type.identifier, expected_op.right_type.identifier)
            raise CompilerError.MismatchedTypes(0, 0, expected_types, actual_types)

    def visit_UnaryOp(self, un_op: ast.UnaryOp) -> Optional[IType]:
        """
        Verifies if the type of the operand is valid to the operation

        If the operation is valid, changes de Python operator by the Boa operator in the syntax tree

        :param un_op: the python ast unary operation node
        :return: the type of the result of the operation if the operation is valid. Otherwise, returns None
        :rtype: IType or None
        """
        operator: Operator = self.get_operator(un_op.op)
        operand = self.visit(un_op.operand)

        if not isinstance(operator, Operator):
            # the operator is invalid or it was not implemented yet
            self._log_error(
                CompilerError.UnresolvedReference(un_op.lineno, un_op.col_offset, type(un_op.op).__name__)
            )

        try:
            operation: UnaryOperation = self.get_un_op(operator, operand)
            if operation is None:
                self._log_error(
                    CompilerError.NotSupportedOperation(un_op.lineno, un_op.col_offset, operator)
                )
            elif not operation.is_supported:
                self._log_error(
                    CompilerError.NotSupportedOperation(un_op.lineno, un_op.col_offset, operator)
                )
            else:
                un_op.op = operation
                return operation.result
        except CompilerError.MismatchedTypes as raised_error:
            expected_types = raised_error.args[2]
            actual_types = raised_error.args[3]
            # raises the exception with the line/col info
            self._log_error(
                CompilerError.MismatchedTypes(un_op.lineno, un_op.col_offset, expected_types, actual_types)
            )

    def get_un_op(self, operator: Operator, operand: Any) -> UnaryOperation:
        """
        Returns the binary operation specified by the operator and the types of the operands

        :param operator: the operator
        :param operand: the operand

        :return: Returns the corresponding :class:`UnaryOperation` if the types are valid.
        :raise MismatchedTypes: raised if the types aren't valid for the operator
        """
        op_type: IType = self.get_type(operand)

        actual_type: str = op_type.identifier
        operation: UnaryOperation = UnaryOp.validate_type(operator, op_type)

        if operation is not None:
            return operation
        else:
            expected_op: UnaryOperation = UnaryOp.get_operation_by_operator(operator)
            expected_type: str = expected_op.operand_type.identifier
            raise CompilerError.MismatchedTypes(0, 0, expected_type, actual_type)

    def visit_Compare(self, compare: ast.Compare) -> Optional[IType]:
        """
        Verifies if the types of the operands are valid to the compare operations

        If the operations are valid, changes de Python operator by the Boa operator in the syntax tree

        :param compare: the python ast compare operation node
        :return: the type of the result of the operation if the operation is valid. Otherwise, returns None
        :rtype: IType or None
        """
        if len(compare.ops) > 1:
            # TODO: implement when logical operations are implemented
            raise NotImplementedError

        if len(compare.comparators) != len(compare.ops):
            self._log_error(
                CompilerError.IncorrectNumberOfOperands(
                    compare.lineno,
                    compare.col_offset,
                    len(compare.ops),
                    len(compare.comparators) + 1    # num comparators + compare.left
                )
            )

        line = compare.lineno
        col = compare.col_offset
        try:
            return_type = None
            l_operand = self.visit(compare.left)
            for index, op in enumerate(compare.ops):
                operator: Operator = self.get_operator(op)
                r_operand = self.visit(compare.comparators[index])

                if not isinstance(operator, Operator):
                    # the operator is invalid or it was not implemented yet
                    self._log_error(
                        CompilerError.UnresolvedReference(line, col, type(op).__name__)
                    )

                operation: BinaryOperation = self.get_bin_op(operator, r_operand, l_operand)
                if operation is None:
                    self._log_error(
                        CompilerError.NotSupportedOperation(line, col, operator)
                    )
                elif not operation.is_supported:
                    # TODO: is, is not and eq were not implemented yet
                    self._log_error(
                        CompilerError.NotSupportedOperation(line, col, operator)
                    )
                else:
                    compare.ops[index] = operation
                    return_type = operation.result

                line = compare.comparators[index].lineno
                col = compare.comparators[index].col_offset
                l_operand = r_operand

            return return_type
        except CompilerError.MismatchedTypes as raised_error:
            expected_types = raised_error.args[2]
            actual_types = raised_error.args[3]
            self._log_error(
                CompilerError.MismatchedTypes(line, col, expected_types, actual_types)
            )

    def get_operator(self, node: ast.AST) -> Optional[Operator]:
        """
        Gets the :class:`Operator` equivalent to given Python ast operator

        :param node: Python ast node
        :return: the Boa operator equivalent to the node. None if it doesn't exit.
        :rtype: Operator or None
        """
        node_type = type(node)
        if node_type in self.__operators:
            return self.__operators[node_type]
        else:
            return None

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

    def visit_Str(self, str: ast.Str) -> str:
        """
        Visitor of literal string node

        :param str: the python ast string node
        :return: the value of the string
        """
        return str.s

    def visit_NameConstant(self, constant: ast.NameConstant) -> Any:
        """
        Visitor of constant names node

        :param constant: the python ast name constant node
        :return: the value of the constant
        """
        return constant.value

    def visit_Name(self, name: ast.Name) -> ast.Name:
        """
        Visitor of a name node

        :param name:
        :return: the object with the name node information
        """
        return name
