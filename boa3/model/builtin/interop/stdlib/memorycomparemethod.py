from typing import Dict

from boa3.model.builtin.interop.nativecontract import StdLibMethod
from boa3.model.variable import Variable


class MemoryCompareMethod(StdLibMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'memory_compare'
        syscall = 'memoryCompare'
        args: Dict[str, Variable] = {
            'mem1': Variable(Type.union.build([Type.bytes, Type.str])),
            'mem2': Variable(Type.union.build([Type.bytes, Type.str]))
        }

        super().__init__(identifier, syscall, args, return_type=Type.int)
