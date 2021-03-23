from typing import Dict

from boa3.model.builtin.interop.binary.stdlibmethod import StdLibMethod
from boa3.model.variable import Variable


class Base64DecodeMethod(StdLibMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'base64_decode'
        syscall = 'base64Decode'
        args: Dict[str, Variable] = {'key': Variable(Type.str)}
        super().__init__(identifier, syscall, args, return_type=Type.bytes)
