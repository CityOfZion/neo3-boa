from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class DeserializeMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'deserialize'
        syscall = 'System.Binary.Deserialize'
        args: Dict[str, Variable] = {'data': Variable(Type.bytes)}
        super().__init__(identifier, syscall, args, return_type=Type.any)
