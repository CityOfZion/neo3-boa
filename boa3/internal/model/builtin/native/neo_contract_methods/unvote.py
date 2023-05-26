from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.internal.model.variable import Variable


class UnVoteMethod(NeoContractMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

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

    def generate_internal_opcodes(self, code_generator):
        # unvote(account) = vote(account, None)
        code_generator.convert_literal(None)
        code_generator.swap_reverse_stack_items(2)
        super().generate_internal_opcodes(code_generator)
