from typing import Dict, List, Tuple

from boa3.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class UnVoteMethod(NeoContractMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        from boa3.model.type.collection.sequence.ecpointtype import ECPointType
        from boa3.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'un_vote'
        native_identifier = 'vote'  # un_vote is not neo native
        args: Dict[str, Variable] = {
            'account': Variable(UInt160Type.build()),
        }

        neo_internal_args = {
            'account': Variable(UInt160Type.build()),
            'vote_to': Variable(ECPointType.build())
        }

        super().__init__(identifier, native_identifier, args, return_type=Type.bool,
                         internal_call_args=len(neo_internal_args))

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        return (
            [
                (Opcode.PUSHNULL, b''),
                (Opcode.SWAP, b''),
            ] +
            super()._opcode
        )
