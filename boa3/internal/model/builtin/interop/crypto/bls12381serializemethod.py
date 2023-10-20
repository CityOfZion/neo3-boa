from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class Bls12381SerializeMethod(CryptoLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.builtin.interop.crypto import Bls12381Type

        identifier = 'bls12_381_serialize'
        native_identifier = 'bls12381Serialize'
        args: Dict[str, Variable] = {
            'g': Variable(Bls12381Type.build()),
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.bytes)
