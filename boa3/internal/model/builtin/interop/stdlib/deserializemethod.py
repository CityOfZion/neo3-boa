from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable


class DeserializeMethod(StdLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'deserialize'
        native_identifier = 'deserialize'
        args: dict[str, Variable] = {'data': Variable(Type.bytes)}
        super().__init__(identifier, native_identifier, args, return_type=Type.any)
