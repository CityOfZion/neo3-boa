from typing import Dict

from boa3.model.builtin.interop.binary.stdlibmethod import StdLibMethod
from boa3.model.variable import Variable


class Base58DecodeMethod(StdLibMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'base58_decode'
        syscall = 'base58Decode'
        args: Dict[str, Variable] = {'key': Variable(Type.str)}
        super().__init__(identifier, syscall, args, return_type=Type.bytes)
