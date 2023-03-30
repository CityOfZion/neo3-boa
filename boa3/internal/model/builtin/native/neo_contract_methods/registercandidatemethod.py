from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.internal.model.variable import Variable


class RegisterCandidateMethod(NeoContractMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType

        identifier = 'register_candidate'
        native_identifier = 'registerCandidate'
        args: Dict[str, Variable] = {
            'pubkey': Variable(ECPointType.build())
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.bool)
