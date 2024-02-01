from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class Bls12381PairingMethod(CryptoLibMethod):

    def __init__(self):
        from boa3.internal.model.builtin.interop.crypto import Bls12381Type

        bls12_381_type = Bls12381Type.build()

        identifier = 'bls12_381_pairing'
        native_identifier = 'bls12381Pairing'
        args: Dict[str, Variable] = {
            'g1': Variable(bls12_381_type),
            'g2': Variable(bls12_381_type),
        }
        super().__init__(identifier, native_identifier, args, return_type=bls12_381_type)
