from typing import Dict

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class GetRandomMethod(InteropMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'get_random'
        syscall = 'System.Runtime.GetRandom'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.int)
