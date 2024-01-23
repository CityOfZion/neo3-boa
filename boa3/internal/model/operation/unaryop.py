from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.operation.unary import *
from boa3.internal.model.operation.unary.unaryoperation import UnaryOperation
from boa3.internal.model.type.itype import IType


class UnaryOp:
    # Arithmetic operations
    Positive = Positive()
    Negative = Negative()

    # Logical operations
    Not = BooleanNot()
    BitNot = LogicNot()

    @classmethod
    def validate_type(cls, operator: Operator, operand: IType) -> UnaryOperation | None:
        """
        Gets a unary operation given the operator and the operand type.

        :param operator: unary operator
        :param operand: type of the operand
        :return: The operation if exists. None otherwise;
        :rtype: UnaryOperation or None
        """
        for id, op in vars(cls).items():
            if isinstance(op, UnaryOperation) and op.is_valid(operator, operand):
                return op.build(operand)

    @classmethod
    def get_operation_by_operator(cls, operator: Operator) -> UnaryOperation | None:
        """
        Gets a unary operation given the operator.

        :param operator: unary operator
        :return: The operation if exists. If exists more than one operation with the same operator, returns the first
        found. None otherwise.
        :rtype: UnaryOperation or None
        """
        for id, op in vars(cls).items():
            if isinstance(op, UnaryOperation) and op.operator is operator:
                return op

    @classmethod
    def get_operation(cls, operation: UnaryOperation) -> UnaryOperation | None:
        """
        Gets an unary operation given another operation.

        :param operation: unary operation
        :return: The operation if exists. None otherwise;
        :rtype: UnaryOperation or None
        """
        for id, op in vars(cls).items():
            if type(operation) == type(op):
                return op
