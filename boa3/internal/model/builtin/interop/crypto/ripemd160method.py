from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class Ripemd160Method(CryptoLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'ripemd160'
        native_identifier = 'ripemd160'
        args: dict[str, Variable] = {'key': Variable(Type.any)}
        super().__init__(identifier, native_identifier, args, return_type=Type.bytes)
