from typing import Dict

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class GetCurrentHeightMethod(InteropMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        identifier = '-get_current_height'
        syscall = 'System.Blockchain.GetHeight'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.int)


class CurrentHeightProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'current_height'
        getter = GetCurrentHeightMethod()
        super().__init__(identifier, getter)
