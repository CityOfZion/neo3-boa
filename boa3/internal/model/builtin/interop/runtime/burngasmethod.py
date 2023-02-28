from typing import Dict

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class BurnGasMethod(InteropMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'burn_gas'
        syscall = 'System.Runtime.BurnGas'
        args: Dict[str, Variable] = {'gas': Variable(Type.int)}
        super().__init__(identifier, syscall, args, return_type=Type.none)
