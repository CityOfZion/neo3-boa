import ast
from typing import Dict

from boa3.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.model.variable import Variable


class UnVoteMethod(NeoContractMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        from boa3.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'un_vote'
        native_identifier = 'vote'
        args: Dict[str, Variable] = {
            'account': Variable(UInt160Type.build()),
            'vote_to': Variable(Type.none)
        }

        args_default = ast.parse("{0}".format(Type.none.default_value)).body[0].value

        super().__init__(identifier, native_identifier, args, defaults=[args_default], return_type=Type.bool)
