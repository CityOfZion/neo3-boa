from boa3.internal.model.builtin.method.builtinevent import IBuiltinEvent
from boa3.internal.model.variable import Variable


class Nep11TransferEvent(IBuiltinEvent):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'Nep11TransferEvent'
        type_token_id = Type.union.build([Type.str, Type.bytes])

        args: dict[str, Variable] = {
            'from_addr': Variable(Type.union.build([Type.none, UInt160Type.build()])),
            'to_addr': Variable(Type.union.build([Type.none, UInt160Type.build()])),
            'amount': Variable(Type.int),
            'tokenId': Variable(type_token_id),
        }
        super().__init__(identifier, args)
        self.name = 'Transfer'
