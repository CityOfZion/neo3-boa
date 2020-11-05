from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class Base64EncodeMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'base64_encode'
        syscall = 'System.Binary.Base64Encode'
        args: Dict[str, Variable] = {'key': Variable(Type.bytes)}
        super().__init__(identifier, syscall, args, return_type=Type.str)
