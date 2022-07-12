from typing import List, Tuple

from boa3.model.builtin.method.printmethod import PrintMethod
from boa3.neo.vm.opcode.Opcode import Opcode


class PrintIntMethod(PrintMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        arg_value = Type.int

        super().__init__(arg_value)

    @property
    def print_value_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        if self._print_value_opcodes is None:
            from boa3.model.builtin.interop.interop import Interop
            itoa_method = Interop.Itoa
            self._print_value_opcodes = (
                [
                    Opcode.get_push_and_data(1),
                    (Opcode.PACK, b'')
                ] +
                itoa_method.opcode.copy()
            )

        return super().print_value_opcodes
