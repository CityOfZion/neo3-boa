from typing import Any, Sized, Iterable

from boa3.internal.model.builtin.interop.storage.get.istoragegetmethod import IStorageGetMethod
from boa3.internal.model.builtin.interop.storage.neostorageinterop import StorageLocalGet
from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class StorageGetBytesMethod(IStorageGetMethod):
    def __init__(self, storage_interop=None):
        identifier = 'get'
        value_type = Type.bytes

        super().__init__(identifier, value_type=value_type, storage_interop=storage_interop)

    def generate_default_value_opcodes(self, code_generator):
        # default_value = b''
        code_generator.convert_literal(b'')

    def generate_deserialize_value_opcodes(self, code_generator):
        # it doesn't need to deserialize bytes values
        return

    def build(self, value: Any) -> IBuiltinMethod:
        exp: list[IExpression] = []
        if isinstance(value, Sized):
            if not isinstance(value, Iterable):
                return self
            exp = [exp if isinstance(exp, IExpression) else Variable(exp)
                   for exp in value if isinstance(exp, (IExpression, IType))]

        if len(exp) == 1:
            return StorageGetBytesMethod(StorageLocalGet())
        else:
            return self
