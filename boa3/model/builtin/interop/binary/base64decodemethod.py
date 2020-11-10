from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class Base64DecodeMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'base64_decode'
        syscall = 'System.Binary.Base64Decode'
        args: Dict[str, Variable] = {'key': Variable(Type.str)}
        super().__init__(identifier, syscall, args, return_type=Type.bytes)
