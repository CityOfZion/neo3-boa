from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class ScriptContainerMethod(InteropMethod):
    def __init__(self):
        identifier = '-get_script_container'
        syscall = 'System.Runtime.GetScriptContainer'
        args: dict[str, Variable] = {}
        from boa3.internal.model.builtin.interop.blockchain import TransactionType
        super().__init__(identifier, syscall, args, return_type=TransactionType.build())


class ScriptContainerProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'script_container'
        getter = ScriptContainerMethod()
        super().__init__(identifier, getter)
