from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class Bls12381DeserializeMethod(CryptoLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'bls12_381_deserialize'
        native_identifier = 'bls12381Deserialize'
        args: Dict[str, Variable] = {
            'data': Variable(Type.bytes),
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.any)
