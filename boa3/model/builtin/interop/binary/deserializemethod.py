from typing import Dict

from boa3.model.builtin.interop.binary.stdlibmethod import StdLibMethod
from boa3.model.variable import Variable


class DeserializeMethod(StdLibMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'deserialize'
        syscall = 'deserialize'
        args: Dict[str, Variable] = {'data': Variable(Type.bytes)}
        super().__init__(identifier, syscall, args, return_type=Type.any)
