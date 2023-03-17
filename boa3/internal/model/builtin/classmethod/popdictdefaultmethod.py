from typing import Dict, List, Optional, Tuple

from boa3.internal.model.builtin.classmethod.popmethod import PopMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class PopDictDefaultMethod(PopMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.internal.model.type.type import Type

        if not Type.dict.is_type_of(arg_value):
            arg_value = Type.dict

        args: Dict[str, Variable] = {
            'self': Variable(arg_value),
            'key': Variable(arg_value.valid_key),
            'default': Variable(Type.any)
        }

        super().__init__(args, return_type=arg_value.value_type)

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.neo.vm.type.Integer import Integer
        from boa3.internal.compiler.codegenerator import get_bytes_count

        jmp_place_holder = (Opcode.JMP, b'\x01')

        put_default_at_bottom = [
            (Opcode.REVERSE3, b''),
            (Opcode.SWAP, b''),
            (Opcode.REVERSE3, b''),
        ]

        prepare_values = [
            (Opcode.DUP, b''),
            (Opcode.SIGN, b''),
            (Opcode.PUSHM1, b''),
            (Opcode.JMPNE, Integer(5).to_byte_array(min_length=1, signed=True)),
            (Opcode.OVER, b''),
            (Opcode.SIZE, b''),
            (Opcode.ADD, b''),
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),
        ]

        verify_has_key = [
            (Opcode.HASKEY, b''),
            jmp_place_holder
        ]

        pick_from_dict = [
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),
            (Opcode.PICKITEM, b''),
            (Opcode.REVERSE3, b''),
            (Opcode.SWAP, b''),
        ]

        pop_from_dict = [
            (Opcode.REMOVE, b''),
            (Opcode.NIP, b''),
            jmp_place_holder
        ]

        return_default = [
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
        ]

        num_jmp_code = get_bytes_count(return_default)
        pop_from_dict[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMP, num_jmp_code, True)

        num_jmp_code = get_bytes_count(pick_from_dict + pop_from_dict)
        verify_has_key[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, num_jmp_code, True)

        return (
            put_default_at_bottom +
            prepare_values +
            verify_has_key +
            pick_from_dict +
            pop_from_dict +
            return_default
        )
