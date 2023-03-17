from typing import Dict, List, Tuple

from boa3.internal.model.builtin.method.listmethod import ListMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ListBytesStringMethod(ListMethod):

    def __init__(self, value: IType = None):
        from boa3.internal.model.type.type import Type

        if value is None:
            value = Type.bytes

        args: Dict[str, Variable] = {
            'value': Variable(value),
        }

        return_type = Type.list.build_collection(value if value is Type.str else Type.int)

        super().__init__(args, return_type)

    @property
    def prepare_for_packing(self) -> List[Tuple[Opcode, bytes]]:

        if self._prepare_for_packing is None:
            from boa3.internal.compiler.codegenerator import get_bytes_count
            from boa3.internal.neo.vm.type.StackItem import StackItemType
            from boa3.internal.model.type.type import Type

            initialize_values = [
                (Opcode.DUP, b''),
                (Opcode.SIZE, b''),
                (Opcode.DEC, b''),
            ]

            loop_for_char_or_byte = [
                (Opcode.OVER, b''),
                (Opcode.OVER, b''),
                (Opcode.PICKITEM, b''),
            ]

            if self._arg_value.type is Type.str:
                loop_for_char_or_byte.append((Opcode.CONVERT, StackItemType.ByteString))

            loop_for_char_or_byte.extend([(Opcode.ROT, b''),
                                          (Opcode.ROT, b''),
                                          (Opcode.DEC, b'')])

            verify_loop_end = [
                (Opcode.DUP, b''),
                (Opcode.SIGN, b''),
                (Opcode.PUSH0, b''),
                # jumps to the beginning of the loop
            ]

            remove_extra_values = [
                (Opcode.DROP, b''),
                (Opcode.SIZE, b''),
            ]

            num_jmp_code = -get_bytes_count(verify_loop_end + loop_for_char_or_byte)
            jmp_to_dec_statement = OpcodeHelper.get_jump_and_data(Opcode.JMPGE, num_jmp_code)
            verify_loop_end.append(jmp_to_dec_statement)

            self._prepare_for_packing = (
                initialize_values +
                loop_for_char_or_byte +
                verify_loop_end +
                remove_extra_values
            )

        return super().prepare_for_packing
