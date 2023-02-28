from typing import List, Tuple

from boa3.internal.model.builtin.method.printmethod import PrintMethod
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class PrintIntMethod(PrintMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        arg_value = Type.int

        super().__init__(arg_value)

    @property
    def print_value_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        if self._print_value_opcodes is None:
            from boa3.internal.model.builtin.interop.stdlib.itoamethod import ItoaMethod
            itoa_method = ItoaMethod(internal_call_args=1)
            self._print_value_opcodes = (
                itoa_method.opcode.copy()
            )

        return super().print_value_opcodes
