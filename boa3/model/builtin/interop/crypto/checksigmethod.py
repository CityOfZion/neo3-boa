from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class CheckSigMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        from boa3.model.type.collection.sequence.ecpointtype import ECPointType

        identifier = 'check_sig'
        syscall = 'System.Crypto.CheckSig'
        args: Dict[str, Variable] = {
            'pubkeys': Variable(ECPointType.build()),
            'signatures': Variable(Type.bytes)
        }
        super().__init__(identifier, syscall, args, return_type=Type.bool)
