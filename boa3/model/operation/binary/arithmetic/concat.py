from typing import List, Tuple

from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType, Type
from boa3.neo.vm.opcode.Opcode import Opcode


class Concat(BinaryOperation):
    """
    A class used to represent a string concatenation operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: List[IType] = [Type.str, Type.bytes]

    def __init__(self, left: IType = Type.str, right: IType = None):
        self.operator: Operator = Operator.Plus
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        if left == right and any(valid_type.is_type_of(left) for valid_type in self._valid_types):
            return True

        left_valid_type = next((valid_type for valid_type in self._valid_types
                                if valid_type.is_type_of(left)), None)
        if left_valid_type is None:
            return False

        right_valid_type = next((valid_type for valid_type in self._valid_types
                                 if valid_type.is_type_of(right)), None)

        return right_valid_type is not None and left_valid_type == right_valid_type

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return left
        else:
            return Type.none

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        codes = [(Opcode.CAT, b'')]

        if Type.str.is_type_of(self.left_type) and Type.str.is_type_of(self.right_type):
            codes.append(
                (Opcode.CONVERT, Type.str.stack_item)
            )
        return codes
