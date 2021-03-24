from typing import Dict

from boa3.model.builtin.interop.binary.stdlibmethod import StdLibMethod
from boa3.model.variable import Variable


class Base58EncodeMethod(StdLibMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'base58_encode'
        syscall = 'base58Encode'
        args: Dict[str, Variable] = {'key': Variable(Type.bytes)}
        super().__init__(identifier, syscall, args, return_type=Type.str)
