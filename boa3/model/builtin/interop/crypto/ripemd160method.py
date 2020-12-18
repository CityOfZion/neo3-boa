from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class Ripemd160Method(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'ripemd160'
        syscall = 'Neo.Crypto.RIPEMD160'
        args: Dict[str, Variable] = {'key': Variable(Type.any)}
        super().__init__(identifier, syscall, args, return_type=Type.bytes)
