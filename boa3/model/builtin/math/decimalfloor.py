from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class DecimalFloorMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'floor'
        args: Dict[str, Variable] = {'x': Variable(Type.int),
                                     'decimals': Variable(Type.int)}
        super().__init__(identifier, args, return_type=Type.int)

    @property
    def exception_message(self) -> str:
        return "decimals cannot be negative"

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.compiler.codegenerator import get_bytes_count
        from boa3.neo.vm.type.Integer import Integer
        from boa3.neo.vm.type.String import String

        message = String(self.exception_message).to_bytes()

        if_negative_decimal = [
            (Opcode.PUSHDATA1, Integer(len(message)).to_byte_array(signed=True, min_length=1) + message),
            (Opcode.THROW, b''),
        ]

        decimals_unit = [
            (Opcode.OVER, b''),
            (Opcode.PUSH0, b''),
            Opcode.get_jump_and_data(Opcode.JMPGE, get_bytes_count(if_negative_decimal), True),
        ] + if_negative_decimal + [
            (Opcode.DUP, b''),
            (Opcode.REVERSE3, b''),
            Opcode.get_push_and_data(10),
            (Opcode.SWAP, b''),
            (Opcode.POW, b''),
            (Opcode.SWAP, b''),
            (Opcode.OVER, b''),
            (Opcode.MOD, b'')
        ]

        if_negative_mod = [
            (Opcode.ADD, b''),
            (Opcode.JMP, b'')
        ]
        else_negative_mod = [
            (Opcode.NIP, b'')
        ]
        num_jmp_code = get_bytes_count(else_negative_mod)
        if_negative_mod[-1] = Opcode.get_jump_and_data(Opcode.JMP, num_jmp_code, True)

        num_jmp_code = get_bytes_count(if_negative_mod)
        floor_computation = [
            (Opcode.DUP, b''),
            (Opcode.PUSH0, b''),
            Opcode.get_jump_and_data(Opcode.JMPGE, num_jmp_code, True),
        ] + if_negative_mod + else_negative_mod + [
            (Opcode.SUB, b'')
        ]

        return decimals_unit + floor_computation

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
