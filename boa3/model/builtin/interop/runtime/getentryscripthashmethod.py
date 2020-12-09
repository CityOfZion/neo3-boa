from typing import Dict, List, Tuple

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class GetEntryScriptHashMethod(InteropMethod):
    def __init__(self):
        from boa3.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_entry_script_hash'
        syscall = 'System.Runtime.GetEntryScriptHash'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=UInt160Type.build())

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.type.type import Type

        opcodes = super().opcode
        opcodes.extend([
            (Opcode.CONVERT, Type.bytes.stack_item)
        ])
        return opcodes


class EntryScriptHashProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'entry_script_hash'
        getter = GetEntryScriptHashMethod()
        super().__init__(identifier, getter)
