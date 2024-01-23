from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable


class Base64EncodeMethod(StdLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'base64_encode'
        native_identifier = 'base64Encode'
        args: dict[str, Variable] = {'key': Variable(Type.bytes)}
        super().__init__(identifier, native_identifier, args, return_type=Type.str)
