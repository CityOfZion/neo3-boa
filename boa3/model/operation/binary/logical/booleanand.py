from typing import List, Tuple

from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType, Type
from boa3.neo.vm.opcode.Opcode import Opcode


class BooleanAnd(BinaryOperation):
    """
    A class used to represent the boolean or operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: List[IType] = [Type.bool]

    def __init__(self, left: IType = Type.bool, right: IType = None):
        self.operator: Operator = Operator.And
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        return left == right and any(_type.is_type_of(left) for _type in self._valid_types)

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return Type.bool
        else:
            return Type.none

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.BOOLAND, b'')]
