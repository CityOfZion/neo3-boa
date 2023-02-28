from typing import Dict

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class CheckMultisigMethod(InteropMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType

        identifier = 'check_multisig'
        syscall = 'System.Crypto.CheckMultisig'
        args: Dict[str, Variable] = {
            'pubkeys': Variable(Type.list.build_collection([ECPointType.build()])),
            'signatures': Variable(Type.list.build_collection([Type.bytes]))
        }
        super().__init__(identifier, syscall, args, return_type=Type.bool)
