from typing import Dict

from boa3.model.builtin.method.builtinevent import IBuiltinEvent
from boa3.model.type.primitive.bytestringtype import ByteStringType
from boa3.model.variable import Variable


class Nep11TransferEvent(IBuiltinEvent):

    def __init__(self):
        from boa3.model.type.type import Type
        from boa3.model.type.collection.sequence.uint160type import UInt160Type
        identifier = 'Nep11TransferEvent'
        args: Dict[str, Variable] = {
            'from_addr': Variable(Type.union.build([Type.none, UInt160Type.build()])),
            'to_addr': Variable(Type.union.build([Type.none, UInt160Type.build()])),
            'amount': Variable(Type.int),
            'tokenId': Variable(ByteStringType.build()),
        }
        super().__init__(identifier, args)
        self.name = 'Transfer'
