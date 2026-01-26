from typing import Any, Sized, Iterable

from boa3.internal.model.builtin.interop.storage.neostorageinterop import StorageLocalPut
from boa3.internal.model.builtin.interop.storage.put.istorageputmethod import IStoragePutMethod
from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class StoragePutIntMethod(IStoragePutMethod):
    def __init__(self, storage_interop=None):
        identifier = 'put_int'
        value_type = Type.int

        super().__init__(identifier, value_type=value_type, storage_interop=storage_interop)

    @property
    def warning_message(self) -> str | None:
        return ("this method uses little-endian and signed representation by default, "
                "it also automatically calculates the length. "
                "See the method documentation for more details.")

    def generate_serialize_value_opcodes(self, code_generator):
        # it doesn't need to serialize primitive types values on put
        return

    def build(self, value: Any) -> IBuiltinMethod:
        exp: list[IExpression] = []
        if isinstance(value, Sized):
            if not isinstance(value, Iterable):
                return self
            exp = [exp if isinstance(exp, IExpression) else Variable(exp)
                   for exp in value if isinstance(exp, (IExpression, IType))]

        if len(exp) == 2:
            return StoragePutIntMethod(StorageLocalPut())
        else:
            return self
