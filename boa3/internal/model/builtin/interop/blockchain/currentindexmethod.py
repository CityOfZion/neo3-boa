from typing import Dict

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.nativecontract import LedgerMethod
from boa3.internal.model.variable import Variable


class GetCurrentIndexMethod(LedgerMethod):
    def __init__(self):
        identifier = 'get_current_index'
        syscall = 'currentIndex'
        args: Dict[str, Variable] = {}
        from boa3.internal.model.type.type import Type
        super().__init__(identifier, syscall, args, return_type=Type.int)


class CurrentIndexProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'current_index'
        getter = GetCurrentIndexMethod()
        super().__init__(identifier, getter)
