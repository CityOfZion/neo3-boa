from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class JsonSerializeMethod(InteropMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'json_serialize'
        syscall = 'System.Json.Serialize'
        args: Dict[str, Variable] = {'item': Variable(Type.any)}
        super().__init__(identifier, syscall, args, return_type=Type.bytes)
