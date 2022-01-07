from typing import List, Tuple

from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType, Type
from boa3.neo.vm.opcode.Opcode import Opcode


class Modulo(BinaryOperation):
    """
    A class used to represent a numeric modulo operation

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: List[IType] = [Type.int]

    def __init__(self, left: IType = Type.int, right: IType = None):
        self.operator: Operator = Operator.Mod
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self.number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        return left == right and any(_type.is_type_of(left) for _type in self._valid_types)

    def _get_result(self, left: IType, right: IType) -> IType:
        if self.validate_type(left, right):
            return left
        else:
            return Type.none

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        jmp_place_holder = (Opcode.JMP, b'')

        mod = [
            (Opcode.SWAP, b''),  # neo's mod has a different result from python's mod in some cases
            (Opcode.OVER, b''),
            (Opcode.MOD, b''),
            (Opcode.DUP, b''),
            (Opcode.SIGN, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.SIGN, b''),
            (Opcode.OVER, b''),      # if the result is not zero and the sign is different than the second operator
            (Opcode.NUMEQUAL, b''),  # the result is different
            (Opcode.SWAP, b''),
            (Opcode.PUSH0, b''),
            (Opcode.NUMEQUAL, b''),  # the result is different
            (Opcode.BOOLOR, b''),
            jmp_place_holder,
        ]

        from boa3.compiler.codegenerator import get_bytes_count
        if_negative = [
            (Opcode.ADD, b''),
            jmp_place_holder
        ]
        num_jmp_code = get_bytes_count(if_negative)
        mod[-1] = Opcode.get_jump_and_data(Opcode.JMPIF, num_jmp_code, True)

        else_negative = [
            (Opcode.NIP, b'')
        ]
        num_jmp_code = get_bytes_count(else_negative)
        if_negative[-1] = Opcode.get_jump_and_data(Opcode.JMP, num_jmp_code, True)

        return mod + if_negative + else_negative
