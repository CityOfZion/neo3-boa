from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable


class HexEncodeMethod(StdLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'hex_encode'
        native_identifier = 'hexEncode'
        args: dict[str, Variable] = {'bytes_': Variable(Type.bytes)}

        super().__init__(identifier, native_identifier, args, return_type=Type.str)
