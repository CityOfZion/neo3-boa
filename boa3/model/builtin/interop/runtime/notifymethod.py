from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class NotifyMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'notify'
        syscall = 'System.Runtime.Notify'
        args: Dict[str, Variable] = {'state': Variable(Type.any)}
        super().__init__(identifier, syscall, args, Type.none)
