from boa3.internal.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.internal.model.variable import Variable


class UnclaimedGasMethod(NeoContractMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'unclaimed_gas'
        native_identifier = 'unclaimedGas'
        args: dict[str, Variable] = {
            'account': Variable(UInt160Type.build()),
            'end': Variable(Type.int)
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.int)
