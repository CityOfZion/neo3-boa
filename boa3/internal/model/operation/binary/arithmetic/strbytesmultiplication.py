from typing import List, Tuple

from boa3.internal.model.builtin.builtin import Builtin
from boa3.internal.model.operation.binary.binaryoperation import BinaryOperation
from boa3.internal.model.operation.operator import Operator
from boa3.internal.model.type.type import IType, Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class StrBytesMultiplication(BinaryOperation):
    """
    A class used to represent a string or bytes concatenation operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: List[IType] = [Type.str, Type.bytes, Builtin.ByteString]

    def __init__(self, left: IType = Type.str, right: IType = Type.int):
        self.operator: Operator = Operator.Mult
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        return any(_type.is_type_of(left) for _type in self._valid_types) and Type.int.is_type_of(right)

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return left
        else:
            return Type.none

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.neo.vm.type.Integer import Integer
        codes = [
            (Opcode.PUSHDATA1, Integer(0).to_byte_array(min_length=1)),  # concatString = ''
            (Opcode.ROT, b''),
            (Opcode.ROT, b''),
            (Opcode.JMP, Integer(7).to_byte_array()),       # while argInt > 0
            (Opcode.REVERSE3, b''),
            (Opcode.OVER, b''),
            (Opcode.CAT, b''),                                  # concatString += argString
            (Opcode.REVERSE3, b''),
            (Opcode.DEC, b''),                                  # argInt -= 1
            (Opcode.DUP, b''),
            (Opcode.PUSH0, b''),
            (Opcode.JMPGT, Integer(-7).to_byte_array()),   # return concatString
            (Opcode.DROP, b''),
            (Opcode.DROP, b'')
        ]
        if Type.str.is_type_of(self.left_type):
            codes.append(
                (Opcode.CONVERT, Type.str.stack_item)
            )
        return codes
