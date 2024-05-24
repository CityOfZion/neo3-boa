from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class Keccak256Method(CryptoLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'keccak256'
        native_identifier = 'keccak256'
        args: dict[str, Variable] = {'key': Variable(Type.bytes)}
        super().__init__(identifier, native_identifier, args, return_type=Type.bytes)
