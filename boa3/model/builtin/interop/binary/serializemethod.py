from typing import Dict

from boa3.model.builtin.interop.binary.stdlibmethod import StdLibMethod
from boa3.model.variable import Variable


class SerializeMethod(StdLibMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'serialize'
        syscall = 'serialize'
        args: Dict[str, Variable] = {'item': Variable(Type.any)}
        super().__init__(identifier, syscall, args, return_type=Type.bytes)
