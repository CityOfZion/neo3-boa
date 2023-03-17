from typing import Dict

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class ScriptContainerMethod(InteropMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = '-get_script_container'
        syscall = 'System.Runtime.GetScriptContainer'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.any)


class ScriptContainerProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'script_container'
        getter = ScriptContainerMethod()
        super().__init__(identifier, getter)
