from typing import Dict

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class GetPlatformMethod(InteropMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = '-get_platform'
        syscall = 'System.Runtime.Platform'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.str)


class PlatformProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'platform'
        getter = GetPlatformMethod()
        super().__init__(identifier, getter)
