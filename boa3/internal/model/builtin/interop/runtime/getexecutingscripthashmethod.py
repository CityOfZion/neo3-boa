from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class GetExecutingScriptHashMethod(InteropMethod):
    def __init__(self):
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_executing_script_hash'
        syscall = 'System.Runtime.GetExecutingScriptHash'
        args: dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=UInt160Type.build())


class ExecutingScriptHashProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'executing_script_hash'
        getter = GetExecutingScriptHashMethod()
        super().__init__(identifier, getter)
