from typing import Optional

from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.binaryop import BinaryOp
from boa3.model.operation.ioperation import IOperation
from boa3.model.operation.unary.unaryoperation import UnaryOperation
from boa3.model.operation.unaryop import UnaryOp


class Operation:
    @classmethod
    def get_operation(cls, operation: IOperation) -> Optional[IOperation]:
        """
        Gets an enum operation given another operations.

        :param operation: an operation
        :return: The operation if exists. None otherwise;
        :rtype: IOperation or None
        """
        if isinstance(operation, BinaryOperation):
            return BinaryOp.get_operation(operation)
        elif isinstance(operation, UnaryOperation):
            return UnaryOp.get_operation(operation)
