from typing import List, Tuple

from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType, Type
from boa3.neo.vm.opcode.Opcode import Opcode


class NotIdentity(BinaryOperation):
    """
    A class used to represent an is not comparison

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: List[IType] = [Type.int]

    def __init__(self, left: IType = Type.int, right: IType = None):
        self.operator: Operator = Operator.IsNot
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        return True

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return Type.bool
        else:
            return Type.none

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [
            (Opcode.NOTEQUAL, b'')
        ]
