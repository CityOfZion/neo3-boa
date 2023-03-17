from typing import Dict

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class LogMethod(InteropMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'log'
        syscall = 'System.Runtime.Log'
        args: Dict[str, Variable] = {'message': Variable(Type.str)}
        super().__init__(identifier, syscall, args, return_type=Type.none)
