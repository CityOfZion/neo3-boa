from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import PolicyContractMethod
from boa3.internal.model.variable import Variable


class IsBlockedMethod(PolicyContractMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'is_blocked'
        native_identifier = 'isBlocked'
        args: Dict[str, Variable] = {
            'account': Variable(UInt160Type.build())
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.bool)
