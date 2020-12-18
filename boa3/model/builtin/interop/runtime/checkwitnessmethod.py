from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class CheckWitnessMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        from boa3.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'check_witness'
        syscall = 'System.Runtime.CheckWitness'
        args: Dict[str, Variable] = {'hash_or_pubkey': Variable(Type.union.build([Type.bytes,
                                                                                  UInt160Type.build()
                                                                                  ]))}
        super().__init__(identifier, syscall, args, return_type=Type.bool)
