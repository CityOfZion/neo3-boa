from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class Base58DecodeMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'base58_decode'
        syscall = 'System.Binary.Base58Decode'
        args: Dict[str, Variable] = {'key': Variable(Type.bytes)}
        super().__init__(identifier, syscall, args, return_type=Type.str)
