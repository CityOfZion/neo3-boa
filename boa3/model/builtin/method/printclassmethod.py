from typing import List, Tuple

from boa3.internal.model.builtin.method.printmethod import PrintMethod
from boa3.internal.model.type.classes.userclass import UserClass
from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class PrintClassMethod(PrintMethod):

    def __init__(self, arg_value: IType):
        if not isinstance(arg_value, UserClass):
            from boa3.internal.model.type.classes import userclass
            arg_value = userclass._EMPTY_CLASS

        super().__init__(arg_value)
        self._arg_type = arg_value

    @property
    def print_value_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        if self._print_value_opcodes is None:

            class_to_dict = [
                (Opcode.UNPACK, b''),
                (Opcode.DROP, b''),
                (Opcode.NEWMAP, b'')
            ]
            for variable_name in self._arg_type.instance_variables:
                class_to_dict.extend([
                    (Opcode.TUCK, b''),
                    OpcodeHelper.get_pushdata_and_data(variable_name),
                    (Opcode.ROT, b''),
                    (Opcode.SETITEM, b'')
                ])

            from boa3.internal.model.builtin.interop.interop import Interop
            self._print_value_opcodes = (
                class_to_dict
                + Interop.JsonSerialize.opcode
            )

        return super().print_value_opcodes
