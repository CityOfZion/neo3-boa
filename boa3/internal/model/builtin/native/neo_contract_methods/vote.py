from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.internal.model.variable import Variable


class VoteMethod(NeoContractMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'vote'
        native_identifier = 'vote'
        args: Dict[str, Variable] = {
            'account': Variable(UInt160Type.build()),
            'vote_to': Variable(ECPointType.build())
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.bool)
