from typing import Dict

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class GetBlockTimeMethod(InteropMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        identifier = '-get_time'
        syscall = 'System.Runtime.GetTime'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.int)


class BlockTimeProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'get_time'
        getter = GetBlockTimeMethod()
        super().__init__(identifier, getter)
