from typing import Any, Sized, Iterable

from boa3.internal.model.builtin.interop.storage.neostorageinterop import StorageLocalPut
from boa3.internal.model.builtin.interop.storage.put.istorageputmethod import IStoragePutMethod
from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class StoragePutUInt160Method(IStoragePutMethod):
    def __init__(self, storage_interop=None):
        identifier = 'put_uint160'
        value_type = UInt160Type.build()

        super().__init__(identifier, value_type=value_type, storage_interop=storage_interop)

    def generate_serialize_value_opcodes(self, code_generator):
        # it doesn't need to serialize UInt160 because it is also bytes value
        return

    def build(self, value: Any) -> IBuiltinMethod:
        exp: list[IExpression] = []
        if isinstance(value, Sized):
            if not isinstance(value, Iterable):
                return self
            exp = [exp if isinstance(exp, IExpression) else Variable(exp)
                   for exp in value if isinstance(exp, (IExpression, IType))]

        if len(exp) == 2:
            return StoragePutUInt160Method(StorageLocalPut())
        else:
            return self
