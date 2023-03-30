from typing import Dict

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class GetCallingScriptHashMethod(InteropMethod):
    def __init__(self):
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_calling_script_hash'
        syscall = 'System.Runtime.GetCallingScriptHash'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=UInt160Type.build())


class CallingScriptHashProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'calling_script_hash'
        getter = GetCallingScriptHashMethod()
        super().__init__(identifier, getter)
