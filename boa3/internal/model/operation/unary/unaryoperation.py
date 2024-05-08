from abc import ABC, abstractmethod
from typing import Self

from boa3.internal.model.operation.operation import IOperation
from boa3.internal.model.type.itype import IType


class UnaryOperation(IOperation, ABC):
    """
    An interface used to represent binary operations

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar operand: the operand type.
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: list[IType] = []

    def __init__(self, operand: IType):
        self.operand_type: IType = operand
        result = self._get_result(operand)
        super().__init__(self.operator, result)

    @property
    def number_of_operands(self) -> int:
        return 1

    @abstractmethod
    def _get_result(self, operand: IType) -> IType:
        """
        Gets the result type of the operation given the operand type.

        :param operand:  operand type
        :return: the result type of the operation. Type.none if the operand is not valid.
        """
        pass

    @classmethod
    def build(cls, operand: IType) -> Self | None:
        """
        Creates a unary operation with the given operand type

        :param operand: operand type
        :return: The built operation if the operands are valid. None otherwise
        :rtype: UnaryOperation or None
        """
        return cls(operand)
