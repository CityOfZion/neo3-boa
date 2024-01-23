from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable


class Base58CheckDecodeMethod(StdLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'base58_check_decode'
        native_identifier = 'base58CheckDecode'
        args: dict[str, Variable] = {'key': Variable(Type.str)}
        super().__init__(identifier, native_identifier, args, return_type=Type.bytes)
