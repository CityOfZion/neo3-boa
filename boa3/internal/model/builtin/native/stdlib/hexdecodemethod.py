from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable


class HexDecodeMethod(StdLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'hex_decode'
        native_identifier = 'hexDecode'
        args: dict[str, Variable] = {'hex_string': Variable(Type.str)}

        super().__init__(identifier, native_identifier, args, return_type=Type.bytes)
