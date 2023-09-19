from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class Bls12381PairingMethod(CryptoLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'bls12_381_pairing'
        native_identifier = 'bls12381Pairing'
        args: Dict[str, Variable] = {
            'g1': Variable(Type.any),
            'g2': Variable(Type.any),
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.any)
