import ast
from typing import Any, Dict, List, Optional, Tuple, Union

from boa3.analyser.astanalyser import IAstAnalyser
from boa3.exception import CompilerError
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.method import Method
from boa3.model.module import Module
from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.binaryop import BinaryOp
from boa3.model.operation.operation import IOperation
from boa3.model.operation.operator import Operator
from boa3.model.operation.unary.unaryoperation import UnaryOperation
from boa3.model.operation.unaryop import UnaryOp
from boa3.model.symbol import ISymbol
from boa3.model.type.sequence.sequencetype import SequenceType
from boa3.model.type.type import IType, Type
from boa3.model.variable import Variable


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
        ast.Div: Operator.Div,
        ast.FloorDiv: Operator.IntDiv,
        ast.Mod: Operator.Mod,
        ast.Pow: Operator.Pow,
        ast.UAdd: Operator.Plus,
        ast.USub: Operator.Minus,
        ast.Eq: Operator.Eq,
        ast.NotEq: Operator.NotEq,
        ast.Lt: Operator.Lt,
        ast.LtE: Operator.LtE,
        ast.Gt: Operator.Gt,
        ast.GtE: Operator.GtE,
        ast.Is: Operator.Is,
        ast.IsNot: Operator.IsNot,
        ast.And: Operator.And,
        ast.Or: Operator.Or,
        ast.Not: Operator.Not,
        ast.BitAnd: Operator.BitAnd,
        ast.BitOr: Operator.BitOr,
        ast.BitXor: Operator.BitXor,
        ast.Invert: Operator.BitNot,
        ast.LShift: Operator.LeftShift,
        ast.RShift: Operator.RightShift
    }

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
        else:
            return super().get_symbol(symbol_id)

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
        if isinstance(method, Method):
            self.__current_method = method

            for stmt in function.body:
                self.visit(stmt)

            if len(function.body) > 0 and not isinstance(function.body[-1], ast.Return):
                default_value: str = str(method.return_type.default_value)
                node: ast.AST = ast.parse(default_value).body[0].value
                function.body.append(
                    ast.Return(lineno=function.lineno, col_offset=function.col_offset, value=node)
                )
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
        ret_value: Any = self.visit(ret.value) if ret.value is not None else None
        ret_type: IType = self.get_type(ret.value)
        if ret.value is not None and ret_type is not Type.none:
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
        if not self.__current_method.return_type.is_type_of(ret_type):
            # if the return type is a specified type sequence, is not a mismatched type when the return expression
            # is an empty sequence
            is_empty_sequence = (
                isinstance(ret_type, SequenceType)
                and ret_type.is_type_of(ret_value)  # if it is a variable or a function, this will be False
                and not isinstance(ret_value, IType)  # if it is an IType value, the latter condition will be True
                and len(ret_value) == 0
            )
            if not (isinstance(self.__current_method.return_type, SequenceType) and is_empty_sequence):
                # the return is None, but the type hint value type is not None
                self._log_error(
                    CompilerError.MismatchedTypes(
                        ret.lineno, ret.col_offset,
                        actual_type_id=ret_type.identifier,
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
        elif isinstance(assign.targets[0], ast.Tuple):
            self._log_error(
                CompilerError.NotSupportedOperation(assign.lineno, assign.col_offset, 'Multiple variable assignments')
            )
        else:
            self.validate_type_variable_assign(assign.targets[0], assign.value)

        # continue to walk through the tree
        self.generic_visit(assign)

    def visit_AnnAssign(self, ann_assign: ast.AnnAssign):
        """
        Verifies if the assigned type is the same as the variable type

        :param ann_assign: the python ast variable annotated assignment node
        """
        # if value is None, it is a declaration
        if ann_assign.value is not None:
            self.validate_type_variable_assign(ann_assign.target, ann_assign.value)

        # continue to walk through the tree
        self.generic_visit(ann_assign)

    def visit_AugAssign(self, aug_assign: ast.AugAssign):
        """
        Verifies if the types of the target variable and the value are compatible with the operation

        If the operation is valid, changes de Python operator by the Boa operator in the syntax tree

        :param aug_assign: the python ast augmented assignment node
        """
        operation = self.validate_binary_operation(aug_assign, aug_assign.target, aug_assign.value)
        if operation is not None:
            # TODO: remove when other augmented assignment operations are implemented
            if operation.result not in [Type.int, Type.str]:
                raise NotImplementedError

            self.validate_type_variable_assign(aug_assign.target, operation)
            aug_assign.op = operation

    def validate_type_variable_assign(self, target: ast.AST, value: Any) -> bool:
        value_type: IType = self.get_type(value)

        if not isinstance(target, ast.Name):
            target_type = self.get_type(target)
        else:
            var: ISymbol = self.get_symbol(target.id)
            if not isinstance(var, Variable):
                self._log_error(
                    CompilerError.UnresolvedReference(
                        target.lineno, target.col_offset,
                        symbol_id=target.id
                    ))
                return False
            if var.type is None:
                # it is an declaration with assignment and the value is neither literal nor another variable
                var.set_type(value_type)
            target_type = var.type

        if not target_type.is_type_of(value_type):
            self._log_error(
                CompilerError.MismatchedTypes(
                    target.lineno, target.col_offset,
                    actual_type_id=value_type.identifier,
                    expected_type_id=target_type.identifier
                ))
            return False

        return True

    def visit_Subscript(self, subscript: ast.Subscript) -> IType:
        """
        Verifies if the subscribed value is a sequence

        :param subscript: the python ast subscript node
        :return: the type of the accessed value if it is valid. Type.none otherwise.
        """
        if isinstance(subscript.slice, ast.Index):
            return self.validate_get_or_set(subscript, subscript.slice)
        elif isinstance(subscript.slice, ast.Slice):
            return self.validate_slice(subscript, subscript.slice)
        return Type.none

    def validate_get_or_set(self, subscript: ast.Subscript, index_node: ast.Index) -> IType:
        """
        Verifies if the subscribed value is a sequence and if the index is valid to this sequence

        :param subscript: the python ast subscript node
        :param index_node: the subscript index
        :return: the type of the accessed value if it is valid. Type.none otherwise.
        """
        value = self.visit(subscript.value)
        index = self.visit(index_node)

        if isinstance(value, ast.Name):
            value = self.get_symbol(value.id)
        if isinstance(index, ast.Name):
            index = self.get_symbol(index.id)

        # if it is a type hint, returns the outer type
        if isinstance(value, IType) and isinstance(index, IType):
            return value

        symbol_type: IType = self.get_type(value)
        index_type: IType = self.get_type(index)

        # only sequence types can be subscribed
        if not isinstance(symbol_type, SequenceType):
            self._log_error(
                CompilerError.UnresolvedOperation(
                    subscript.lineno, subscript.col_offset,
                    type_id=symbol_type.identifier,
                    operation_id=Operator.Subscript)
            )
            return symbol_type
        # the sequence can't use the given type as index
        elif not symbol_type.is_valid_key(index_type):
            self._log_error(
                CompilerError.MismatchedTypes(
                    subscript.lineno, subscript.col_offset,
                    actual_type_id=index_type.identifier,
                    expected_type_id=symbol_type.valid_key.identifier)
            )
        # it is setting a value in a sequence that doesn't allow reassign values
        elif isinstance(subscript.ctx, ast.Store) and not symbol_type.can_reassign_values:
            self._log_error(
                CompilerError.UnresolvedOperation(
                    subscript.lineno, subscript.col_offset,
                    type_id=symbol_type.identifier,
                    operation_id=Operator.Subscript)
            )
        else:
            return symbol_type.value_type
        return Type.none

    def validate_slice(self, subscript: ast.Subscript, slice_node: ast.Slice) -> IType:
        """
        Verifies if the subscribed value is a sequence and if the slice is valid to this sequence

        :param subscript: the python ast subscript node
        :param slice_node: the subscript slice
        :return: the type of the accessed value if it is valid. Type.none otherwise.
        """
        value = self.visit(subscript.value)
        lower, upper, step = (self.get_type(value) for value in self.visit(slice_node))

        if step is not Type.none:
            # TODO: remove when slices with stride are implemented
            raise NotImplementedError
        # is not allowed to store into a slice
        if isinstance(subscript.ctx, ast.Store):
            self._log_error(
                CompilerError.NotSupportedOperation(
                    subscript.lineno, subscript.col_offset,
                    symbol_id=Operator.Subscript
                )
            )

        symbol_type: IType = self.get_type(value)
        # only sequence types can be subscribed
        if not isinstance(symbol_type, SequenceType):
            self._log_error(
                CompilerError.UnresolvedOperation(
                    subscript.lineno, subscript.col_offset,
                    type_id=symbol_type.identifier,
                    operation_id=Operator.Subscript)
            )
            return Type.none

        lower = lower if lower is not Type.none else symbol_type.valid_key
        upper = upper if upper is not Type.none else symbol_type.valid_key

        # TODO: remove when slices of other sequence types are implemented
        if symbol_type is not Type.str:
            expected: IType = symbol_type.valid_key
            actual: Tuple[IType, ...] = (lower, upper) if step is Type.none else (lower, upper, step)
            self._log_error(
                CompilerError.MismatchedTypes(
                    subscript.lineno, subscript.col_offset,
                    expected_type_id=expected.identifier,
                    actual_type_id=[value.identifier for value in actual]
                )
            )
        elif (
            not symbol_type.is_valid_key(lower)
            or not symbol_type.is_valid_key(upper)
            or (step is not Type.none and not symbol_type.is_valid_key(step))
        ):
            actual: Tuple[IType, ...] = (lower, upper) if step is Type.none else (lower, upper, step)
            self._log_error(
                CompilerError.MismatchedTypes(
                    subscript.lineno, subscript.col_offset,
                    expected_type_id=[symbol_type.valid_key.identifier for value in actual],
                    actual_type_id=[value.identifier for value in actual]
                )
            )
        else:
            return symbol_type

        return Type.none

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

    def visit_For(self, for_node: ast.For):
        """
        Verifies if the type of for iterator is valid

        :param for_node: the python ast for node
        """
        iterator = self.visit(for_node.iter)
        iterator_type: IType = self.get_type(iterator)

        if not isinstance(iterator_type, SequenceType):
            self._log_error(
                CompilerError.MismatchedTypes(
                    for_node.lineno, for_node.col_offset,
                    actual_type_id=iterator_type.identifier,
                    expected_type_id=Type.sequence.identifier)
            )
        elif iterator_type is Type.str:
            # TODO: remove when iteration in strings is implemented
            raise NotImplementedError

        # continue to walk through the tree
        for stmt in for_node.body:
            self.visit(stmt)
        for stmt in for_node.orelse:
            self.visit(stmt)

    def visit_If(self, if_node: ast.If):
        """
        Verifies if the type of if test is valid

        :param if_node: the python ast if statement node
        """
        self.validate_if(if_node)
        # continue to walk through the tree
        for stmt in if_node.body:
            self.visit(stmt)
        for stmt in if_node.orelse:
            self.visit(stmt)

    def visit_IfExp(self, if_node: ast.IfExp):
        """
        Verifies if the type of if test is valid

        :param if_node: the python ast if expression node
        """
        self.validate_if(if_node)
        body = if_node.body
        orelse = if_node.orelse
        if_value = body[-1] if isinstance(body, list) and len(body) > 0 else body
        else_value = orelse[-1] if isinstance(orelse, list) and len(orelse) > 0 else orelse

        if_type: IType = self.get_type(if_value)
        else_type: IType = self.get_type(else_value)
        return Type.get_generic_type(if_type, else_type)

    def validate_if(self, if_node: ast.AST):
        """
        Verifies if the type of if test is valid

        :param if_node: the python ast if statement node
        :type if_node: ast.If or ast.IfExp
        """
        test = self.visit(if_node.test)
        test_type: IType = self.get_type(test)

        if test_type is not Type.bool:
            self._log_error(
                CompilerError.MismatchedTypes(
                    if_node.lineno, if_node.col_offset,
                    actual_type_id=test_type.identifier,
                    expected_type_id=Type.bool.identifier)
            )

    def visit_BinOp(self, bin_op: ast.BinOp) -> Optional[IType]:
        """
        Verifies if the types of the operands are valid to the operation

        If the operation is valid, changes de Python operator by the Boa operator in the syntax tree

        :param bin_op: the python ast binary operation node
        :return: the type of the result of the operation if the operation is valid. Otherwise, returns None
        :rtype: IType or None
        """
        operation = self.validate_binary_operation(bin_op, bin_op.left, bin_op.right)
        if operation is not None:
            bin_op.op = operation
            return operation.result

    def validate_binary_operation(self, node: ast.AST, left_op: ast.AST, right_op: ast.AST) -> Optional[IOperation]:
        """
        Validates a ast node that represents a binary operation

        :param node: ast node that represents a binary operation
        :param left_op: ast node that represents the left operand of the operation
        :param right_op: ast node that represents the right operand of the operation
        :return: the corresponding :class:`BinaryOperation` if is valid. None otherwise.
        """
        if not hasattr(node, 'op'):
            return

        operator: Operator = self.get_operator(node.op)
        l_operand = self.visit(left_op)
        r_operand = self.visit(right_op)

        if not isinstance(operator, Operator):
            # the operator is invalid or it was not implemented yet
            self._log_error(
                CompilerError.UnresolvedReference(node.lineno, node.col_offset, type(node.op).__name__)
            )

        try:
            operation: IOperation = self.get_bin_op(operator, r_operand, l_operand)
            if operation is None:
                self._log_error(
                    CompilerError.NotSupportedOperation(node.lineno, node.col_offset, operator)
                )
            elif not operation.is_supported:
                # TODO: concat and power not implemented yet
                # number float division is not supported by Neo VM
                self._log_error(
                    CompilerError.NotSupportedOperation(node.lineno, node.col_offset, operator)
                )
            else:
                return operation
        except CompilerError.MismatchedTypes as raised_error:
            raised_error.line = node.lineno
            raised_error.col = node.col_offset
            # raises the exception with the line/col info
            self._log_error(raised_error)

    def get_bin_op(self, operator: Operator, right: Any, left: Any) -> IOperation:
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

        actual_types = (l_type.identifier, r_type.identifier)
        operation: IOperation = BinaryOp.validate_type(operator, l_type, r_type)

        if operation is not None:
            return operation
        else:
            expected_op: BinaryOperation = BinaryOp.get_operation_by_operator(operator, l_type)
            expected_types = (expected_op.left_type.identifier, expected_op.right_type.identifier)
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
            raised_error.line = un_op.lineno
            raised_error.col = un_op.col_offset
            # raises the exception with the line/col info
            self._log_error(raised_error)

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
        if len(compare.comparators) != len(compare.ops):
            self._log_error(
                CompilerError.IncorrectNumberOfOperands(
                    compare.lineno,
                    compare.col_offset,
                    len(compare.ops),
                    len(compare.comparators) + 1  # num comparators + compare.left
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

                operation: IOperation = self.get_bin_op(operator, r_operand, l_operand)
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
            raised_error.line = line
            raised_error.col = col
            # raises the exception with the line/col info
            self._log_error(raised_error)

    def visit_BoolOp(self, bool_op: ast.BoolOp) -> Optional[IType]:
        """
        Verifies if the types of the operands are valid to the boolean operations

        If the operations are valid, changes de Python operator by the Boa operator in the syntax tree

        :param bool_op: the python ast boolean operation node
        :return: the type of the result of the operation if the operation is valid. Otherwise, returns None
        :rtype: IType or None
        """
        lineno: int = bool_op.lineno
        col_offset: int = bool_op.col_offset
        try:
            return_type: IType = None
            bool_operation: IOperation = None
            operator: Operator = self.get_operator(bool_op.op)

            if not isinstance(operator, Operator):
                # the operator is invalid or it was not implemented yet
                self._log_error(
                    CompilerError.UnresolvedReference(lineno, col_offset, type(operator).__name__)
                )

            l_operand = self.visit(bool_op.values[0])
            for index, operand in enumerate(bool_op.values[1:]):
                r_operand = self.visit(operand)

                operation: IOperation = self.get_bin_op(operator, r_operand, l_operand)
                if operation is None:
                    self._log_error(
                        CompilerError.NotSupportedOperation(lineno, col_offset, operator)
                    )
                elif bool_operation is None:
                    return_type = operation.result
                    bool_operation = operation

                lineno = operand.lineno
                col_offset = operand.col_offset
                l_operand = r_operand

            bool_op.op = bool_operation
            return return_type
        except CompilerError.MismatchedTypes as raised_error:
            raised_error.line = lineno
            raised_error.col = col_offset
            # raises the exception with the line/col info
            self._log_error(raised_error)

    def get_operator(self, node: Union[ast.operator, Operator, IOperation]) -> Optional[Operator]:
        """
        Gets the :class:`Operator` equivalent to given Python ast operator

        :param node: object with the operator data
        :type node: ast.operator or Operator or IOperation
        :return: the Boa operator equivalent to the node. None if it doesn't exit.
        :rtype: Operator or None
        """
        # the node has already been visited
        if isinstance(node, Operator):
            return node
        elif isinstance(node, IOperation):
            return node.operator

        node_type = type(node)
        if node_type in self.__operators:
            return self.__operators[node_type]
        else:
            return None

    def visit_Call(self, call: ast.Call):
        """
        Verifies if the number of arguments is correct

        :param call: the python ast function call node
        :return: the result type of the called function
        """
        function = None
        if isinstance(call.func, ast.Name):
            function_id: str = call.func.id
            function = self.get_symbol(function_id)
        else:
            arg0, function, function_id = self.visit(call.func)
            arg0_identifier = self.visit(arg0)
            if isinstance(arg0_identifier, ast.Name):
                arg0_identifier = arg0_identifier.id

            if function is not None and not isinstance(self.get_symbol(arg0_identifier), IType):
                call.args.insert(0, arg0)
            if len(call.args) > 0 and isinstance(function, IBuiltinMethod) and function.has_self_argument:
                self_type: IType = self.get_type(call.args[0])
                function = function.build(self_type)

        if not isinstance(function, Method):
            # the symbol doesn't exists or is not a function
            self._log_error(
                CompilerError.UnresolvedReference(call.func.lineno, call.func.col_offset, function_id)
            )
        else:
            # TODO: change when kwargs is implemented
            if len(call.args) > len(function.args):
                unexpected_arg = call.args[len(function.args)]
                self._log_error(
                    CompilerError.UnexpectedArgument(unexpected_arg.lineno, unexpected_arg.col_offset)
                )
            elif len(call.args) < len(function.args):
                missed_arg = list(function.args)[len(call.args)]
                self._log_error(
                    CompilerError.UnfilledArgument(call.lineno, call.col_offset, missed_arg)
                )
            else:
                for index, (arg_id, arg_value) in enumerate(function.args.items()):
                    param = call.args[index]
                    param_type = self.get_type(param)
                    if not arg_value.type.is_type_of(param_type):
                        self._log_error(
                            CompilerError.MismatchedTypes(
                                param.lineno, param.col_offset,
                                arg_value.type.identifier,
                                param_type.identifier
                            ))
        return self.get_type(function)

    def visit_Attribute(self, attribute: ast.Attribute) -> Tuple[IType, Optional[ISymbol], str]:
        """
        Gets the attribute inside the ast node

        :param attribute: the python ast attribute node
        :return: returns the type of the value, the attribute symbol and its id if the attribute exists.
                 Otherwise, returns None
        """
        value_type: IType = self.get_type(attribute.value)
        attr_symbol: Optional[ISymbol] = self.get_symbol(attribute.attr)

        return attribute.value, attr_symbol, attribute.attr

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

    def visit_Tuple(self, tup_node: ast.Tuple) -> Tuple[Any, ...]:
        """
        Visitor of literal tuple node

        :param tup_node: the python ast tuple node
        :return: the value of the tuple
        """
        return tuple(self.get_type(value) for value in tup_node.elts)

    def visit_List(self, list_node: ast.List) -> List[Any]:
        """
        Visitor of literal list node

        :param list_node: the python ast list node
        :return: the value of the list
        """
        return [self.get_type(value) for value in list_node.elts]

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

    def visit_Index(self, index: ast.Index) -> Any:
        """
        Visitor of an index node

        :param index:
        :return: the object with the index value information
        """
        return self.visit(index.value)

    def visit_Slice(self, slice_node: ast.Slice) -> Tuple[Any, Any, Any]:
        """
        Visitor of an slice node

        :param slice_node:
        :return: the object with the index value information
        """
        return slice_node.lower, slice_node.upper, slice_node.step

    def visit_Break(self, break_node: ast.Break):
        """
        :param break_node: the python ast break statement node
        """
        # TODO: remove when implement break statement
        raise NotImplementedError

    def visit_Continue(self, continue_node: ast.Continue):
        """
        :param continue_node: the python ast continue statement node
        """
        # TODO: remove when implement continue statement
        raise NotImplementedError
