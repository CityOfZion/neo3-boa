from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class Bls12381AddMethod(CryptoLibMethod):

    def __init__(self):
        from boa3.internal.model.builtin.interop.crypto import Bls12381Type
        bls12_381_type = Bls12381Type.build()

        identifier = 'bls12_381_add'
        native_identifier = 'bls12381Add'
        args: dict[str, Variable] = {
            'x': Variable(bls12_381_type),
            'y': Variable(bls12_381_type),
        }
        super().__init__(identifier, native_identifier, args, return_type=bls12_381_type)
