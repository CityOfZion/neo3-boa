from typing import Dict, List, Tuple

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class GetCallingScriptHashMethod(InteropMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        identifier = '-get_calling_script_hash'
        syscall = 'System.Runtime.GetCallingScriptHash'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.bytes)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.type.type import Type

        opcodes = super().opcode
        opcodes.extend([
            (Opcode.CONVERT, Type.bytes.stack_item)
        ])
        return opcodes


class CallingScriptHashProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'calling_script_hash'
        getter = GetCallingScriptHashMethod()
        super().__init__(identifier, getter)
