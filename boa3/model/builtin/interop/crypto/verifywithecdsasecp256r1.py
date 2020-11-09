from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class VerifyWithECDsaSecp256r1Method(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'verify_with_ecdsa_secp256r1'
        syscall = 'Neo.Crypto.VerifyWithECDsaSecp256r1'
        args: Dict[str, Variable] = {
            'item': Variable(Type.any),
            'pubkey': Variable(Type.bytes),
            'signature': Variable(Type.bytes)
        }
        super().__init__(identifier, syscall, args, return_type=Type.bool)
