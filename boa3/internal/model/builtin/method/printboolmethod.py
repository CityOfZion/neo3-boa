from typing import List, Tuple

from boa3.internal.model.builtin.method.printmethod import PrintMethod
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class PrintBoolMethod(PrintMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        arg_value = Type.bool

        super().__init__(arg_value)

    @property
    def print_value_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        if self._print_value_opcodes is None:
            from boa3.internal.model.builtin.interop.interop import Interop
            self._print_value_opcodes = (
                [
                    (Opcode.NZ, b''),
                ] + Interop.JsonSerialize.opcode
            )

        return super().print_value_opcodes
