from typing import List, Tuple

from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType, Type
from boa3.neo.vm.opcode.Opcode import Opcode


class LeftShift(BinaryOperation):
    """
    A class used to represent the bit left shift [ << ] operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: List[IType] = [Type.int, Type.bool]

    def __init__(self, left: IType = Type.int, right: IType = Type.int):
        self.operator: Operator = Operator.LeftShift
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        return left in self._valid_types and right is Type.int

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return left
        else:
            return Type.none

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.SHL, b'')]
