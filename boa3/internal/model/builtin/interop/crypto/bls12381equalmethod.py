from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class Bls12381EqualMethod(CryptoLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'bls12_381_equal'
        native_identifier = 'bls12381Equal'
        args: Dict[str, Variable] = {
            'x': Variable(Type.any),
            'y': Variable(Type.any),
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.bool)
