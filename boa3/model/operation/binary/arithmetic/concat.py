from typing import List, Optional, Tuple

from boa3.model.builtin.builtin import Builtin
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
    _valid_types: List[IType] = [Type.str, Type.bytes, Builtin.ByteString]

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

        left_valid_type = self._get_valid_type(left)
        if left_valid_type is None:
            return False

        right_valid_type = self._get_valid_type(right)

        return (right_valid_type is not None
                and (left_valid_type == right_valid_type
                     or left_valid_type.is_type_of(right_valid_type)
                     or right_valid_type.is_type_of(left_valid_type))
                )

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            left_internal = self._get_valid_type(left)
            right_internal = self._get_valid_type(right)

            if left_internal.is_type_of(Builtin.ByteString):
                # for bytestring + str the result is str and bytestring + bytes is bytes
                return right
            if right_internal.is_type_of(Builtin.ByteString):
                return left

            if right.is_type_of(left):
                return right
            if left.is_type_of(right):
                return left

            return left_internal
        else:
            return Type.none

    def _get_valid_type(self, operator_type: IType) -> Optional[IType]:
        return next((valid_type for valid_type in self._valid_types
                     if valid_type.is_type_of(operator_type)), None)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.CAT, b''),
                (Opcode.CONVERT, Type.str.stack_item)
                ]
