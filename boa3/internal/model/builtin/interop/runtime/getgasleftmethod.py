from typing import Dict

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class GetGasLeftMethod(InteropMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = '-get_gas_left'
        syscall = 'System.Runtime.GasLeft'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.int)


class GasLeftProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'gas_left'
        getter = GetGasLeftMethod()
        super().__init__(identifier, getter)
