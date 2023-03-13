from typing import List, Tuple

from boa3.model.builtin.method.printmethod import PrintMethod
from boa3.model.type.itype import IType
from boa3.neo.vm.opcode.Opcode import Opcode


class PrintSequenceMethod(PrintMethod):

    def __init__(self, arg_value: IType):
        from boa3.model.type.type import Type

        if not isinstance(arg_value, IType) or not Type.sequence.is_type_of(arg_value):
            arg_value = Type.list

        super().__init__(arg_value)

    @property
    def print_value_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        if self._print_value_opcodes is None:
            from boa3.model.builtin.interop.interop import Interop
            self._print_value_opcodes = Interop.JsonSerialize.opcode.copy()

        return super().print_value_opcodes
