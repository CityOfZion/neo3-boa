from typing import Dict

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class GetAddressVersionMethod(InteropMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        identifier = '-get_address_version'
        syscall = 'System.Runtime.GetAddressVersion'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.int)


class AddressVersionProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'address_version'
        getter = GetAddressVersionMethod()
        super().__init__(identifier, getter)
