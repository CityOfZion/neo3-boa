from abc import ABC, abstractmethod
from typing import Optional

from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType
from boa3.neo.vm.Opcode import Opcode


class IOperation(ABC):
    """
    An interface used to represent operations

    :ivar operator: the operator of the operation
    :ivar result: the result type of the operation
    """
    def __init__(self, operator: Operator, result_type: IType):
        self.operator: Operator = operator
        self.result: IType = result_type

    @property
    def opcode(self) -> Optional[Opcode]:
        """
        Gets the operation opcode in Neo Vm

        :return: the opcode if exists. None otherwise.
        """
        return None

    @property
    @abstractmethod
    def _get_number_of_operands(self) -> int:
        """
        Gets the number of operands required for this operations

        :return: Number of operands
        """
        pass

    @abstractmethod
    def validate_type(self, *types: IType) -> bool:
        """
        Verifies if the given operands are valid to the operation

        :param types: types of the operand
        :return: True if all arguments are valid. False otherwise.
        """
        pass

    def is_valid(self, operator: Operator, *types: IType) -> bool:
        """
        Verifies if the given operator and operands are valid to the operation

        :param operator:
        :param types: types of the operand
        :return: True if all arguments are valid. False otherwise.
        """
        if len(types) != self._get_number_of_operands:
            return False

        return operator is self.operator and self.validate_type(*types)
