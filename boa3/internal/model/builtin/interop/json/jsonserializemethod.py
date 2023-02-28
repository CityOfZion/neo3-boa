from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable


class JsonSerializeMethod(StdLibMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'json_serialize'
        native_identifier = 'jsonSerialize'
        args: Dict[str, Variable] = {'item': Variable(Type.any)}
        super().__init__(identifier, native_identifier, args, return_type=Type.str)
