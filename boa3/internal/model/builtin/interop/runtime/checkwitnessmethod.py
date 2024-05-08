from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class CheckWitnessMethod(InteropMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'check_witness'
        syscall = 'System.Runtime.CheckWitness'
        args: dict[str, Variable] = {'hash_or_pubkey': Variable(Type.union.build([ECPointType.build(),
                                                                                  UInt160Type.build()
                                                                                  ]))}
        super().__init__(identifier, syscall, args, return_type=Type.bool)
