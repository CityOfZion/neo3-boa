from abc import ABC, abstractmethod
from typing import List

from boa3.model.operation.operation import IOperation
from boa3.model.type.type import IType


class BinaryOperation(IOperation, ABC):
    """
    An interface used to represent binary operations

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: List[IType] = []

    def __init__(self, left: IType, right: IType):
        self.left_type: IType = left
        self.right_type: IType = right
        result = self._get_result(left, right)
        super().__init__(self.operator, result)

    @property
    def _get_number_of_operands(self) -> int:
        return 2

    @abstractmethod
    def _get_result(self, left: IType, right: IType) -> IType:
        """
        Gets the result type of the operation given the operands types.

        :param left: left operand type
        :param right: right operand type
        :return: the result type of the operation. Type.none if the operands are not valid.
        """
        pass

    @classmethod
    def build(cls, left: IType, right: IType):
        """
        Creates a binary operation with the given operands types

        :param left: left operand type
        :param right: right operand type
        :return: The built operation if the operands are valid. None otherwise
        :rtype: BinaryOperation or None
        """
        return cls(left, right)
