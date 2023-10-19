from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class Bls12381EqualMethod(CryptoLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.builtin.interop.crypto import Bls12381Type

        bls12_381_type = Bls12381Type.build()

        identifier = 'bls12_381_equal'
        native_identifier = 'bls12381Equal'
        args: Dict[str, Variable] = {
            'x': Variable(bls12_381_type),
            'y': Variable(bls12_381_type),
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.bool)
