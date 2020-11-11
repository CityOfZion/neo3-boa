from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class UpdateMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'update_contract'
        syscall = 'System.Contract.Update'
        args: Dict[str, Variable] = {
            'script': Variable(Type.bytes),
            'manifest': Variable(Type.bytes)
        }
        super().__init__(identifier, syscall, args, return_type=Type.any)
