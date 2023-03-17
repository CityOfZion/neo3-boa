from typing import Dict, List, Tuple

from boa3.internal.model.builtin.method.strmethod import StrMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String


class StrBoolMethod(StrMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        args: Dict[str, Variable] = {
            'object': Variable(Type.bool),
        }

        super().__init__(args)

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.compiler.codegenerator import get_bytes_count

        jmp_place_holder = (Opcode.JMP, b'\x01')
        true = String("True").to_bytes()
        false = String("False").to_bytes()

        check_is_true = [
            jmp_place_holder
        ]

        put_false = [
            (Opcode.PUSHDATA1, Integer(len(false)).to_byte_array(signed=True, min_length=1) + false),
            jmp_place_holder
        ]

        put_true = [
            (Opcode.PUSHDATA1, Integer(len(true)).to_byte_array(signed=True, min_length=1) + true),
        ]

        jmp_put_true = OpcodeHelper.get_jump_and_data(Opcode.JMP, get_bytes_count(put_true))
        put_false[-1] = jmp_put_true

        jmp_put_false = OpcodeHelper.get_jump_and_data(Opcode.JMPIF, get_bytes_count(put_false))
        check_is_true[-1] = jmp_put_false

        return (
            check_is_true +
            put_false +
            put_true
        )
