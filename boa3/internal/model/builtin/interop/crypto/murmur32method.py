from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class Murmur32Method(CryptoLibMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'murmur32'
        native_identifier = 'murmur32'
        args: Dict[str, Variable] = {
            'data': Variable(Type.bytes),
            'seed': Variable(Type.int),
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.bytes)
