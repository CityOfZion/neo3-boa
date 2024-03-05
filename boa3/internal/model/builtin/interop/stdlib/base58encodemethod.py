from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable


class Base58EncodeMethod(StdLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'base58_encode'
        native_identifier = 'base58Encode'
        args: dict[str, Variable] = {'key': Variable(Type.bytes)}
        super().__init__(identifier, native_identifier, args, return_type=Type.str)
