from typing import Dict, List, Tuple

from boa3.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class VerifyWithECDsaSecp256k1Method(CryptoLibMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'verify_with_ecdsa_secp256k1'
        native_identifier = 'verifyWithECDsa'
        args: Dict[str, Variable] = {
            'item': Variable(Type.any),
            'pubkey': Variable(Type.bytes),
            'signature': Variable(Type.bytes)
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.bool)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo3.contracts.namedcurve import NamedCurve
        curve = NamedCurve.SECP256K1

        return ([(Opcode.DUP, b''),
                 Opcode.get_push_and_data(curve),
                 (Opcode.APPEND, b'')
                 ]
                + super().opcode)
