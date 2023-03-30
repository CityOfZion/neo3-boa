from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class Sha256Method(CryptoLibMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'sha256'
        native_identifier = 'sha256'
        args: Dict[str, Variable] = {'key': Variable(Type.any)}
        super().__init__(identifier, native_identifier, args, return_type=Type.bytes)
