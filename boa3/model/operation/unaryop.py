from typing import Optional, Dict

from boa3.model.operation.operator import Operator
from boa3.model.operation.unary.negative import Negative
from boa3.model.operation.unary.positive import Positive
from boa3.model.operation.unary.unaryoperation import UnaryOperation
from boa3.model.type.type import IType


class UnaryOp:
    __operations: Dict[str, UnaryOperation] = {
        # Arithmetic operations
        'Positive': Positive(),
        'Negative': Negative()
    }

    # Arithmetic operations
    Positive = __operations['Positive']
    Negative = __operations['Negative']

    @classmethod
    def validate_type(cls, operator: Operator, operand: IType) -> Optional[UnaryOperation]:
        """
        Gets a unary operation given the operator and the operand type.

        :param operator: unary operator
        :param operand: type of the operand
        :return: The operation if exists. None otherwise;
        :rtype: UnaryOperation or None
        """
        for id, op in cls.__operations.items():
            if op.is_valid(operator, operand):
                return op.build(operand)

    @classmethod
    def get_operation_by_operator(cls, operator: Operator) -> Optional[UnaryOperation]:
        """
        Gets a unary operation given the operator.

        :param operator: unary operator
        :return: The operation if exists. If exists more than one operation with the same operator, returns the first
        found. None otherwise.
        :rtype: UnaryOperation or None
        """
        for id, op in cls.__operations.items():
            if op.operator is operator:
                return op

    @classmethod
    def get_operation(cls, operation: UnaryOperation) -> Optional[UnaryOperation]:
        """
        Gets an unary operation given another operation.

        :param operation: unary operation
        :return: The operation if exists. None otherwise;
        :rtype: UnaryOperation or None
        """
        for id, op in cls.__operations.items():
            if type(operation) == type(op):
                return op
