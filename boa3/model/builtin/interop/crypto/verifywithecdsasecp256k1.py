from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class VerifyWithECDsaSecp256k1Method(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'verify_with_ecdsa_secp256k1'
        syscall = 'Neo.Crypto.VerifyWithECDsaSecp256k1'
        args: Dict[str, Variable] = {
            'item': Variable(Type.any),
            'pubkey': Variable(Type.bytes),
            'signature': Variable(Type.bytes)
        }
        super().__init__(identifier, syscall, args, return_type=Type.bool)
