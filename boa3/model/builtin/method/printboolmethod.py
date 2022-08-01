from typing import List, Tuple

from boa3.model.builtin.method.printmethod import PrintMethod
from boa3.neo.vm.opcode.Opcode import Opcode


class PrintBoolMethod(PrintMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        arg_value = Type.bool

        super().__init__(arg_value)

    @property
    def print_value_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        if self._print_value_opcodes is None:
            from boa3.compiler.codegenerator import get_bytes_count
            if_value_is_true = [
                Opcode.get_pushdata_and_data('True')
            ]
            if_value_is_false = [
                Opcode.get_pushdata_and_data('False'),
                Opcode.get_jump_and_data(Opcode.JMP, get_bytes_count(if_value_is_true), jump_through=True)
            ]

            self._print_value_opcodes = (
                [
                    (Opcode.NZ, b''),
                    Opcode.get_jump_and_data(Opcode.JMPIF, get_bytes_count(if_value_is_false), jump_through=True),
                ] + if_value_is_false
                + if_value_is_true
            )

        return super().print_value_opcodes
