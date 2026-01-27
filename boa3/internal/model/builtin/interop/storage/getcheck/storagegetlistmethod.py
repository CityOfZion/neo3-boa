from typing import Any, Sized, Iterable

from boa3.internal.model.builtin.interop.storage.getcheck.istoragetrygetmethod import IStorageTryGetMethod
from boa3.internal.model.builtin.interop.storage.neostorageinterop import StorageLocalGet
from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class StorageTryGetListMethod(IStorageTryGetMethod):
    def __init__(self, storage_interop=None):
        identifier = 'try_get_list'
        value_type = Type.list

        super().__init__(identifier, value_type=value_type, storage_interop=storage_interop)

    def generate_default_value_opcodes(self, code_generator):
        # default_value = []
        code_generator.convert_new_empty_array(0, Type.list)

    def generate_deserialize_value_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.interop import Interop

        converter = Interop.Deserialize
        code_generator.convert_builtin_method_call(converter, is_internal=True)

    def build(self, value: Any) -> IBuiltinMethod:
        exp: list[IExpression] = []
        if isinstance(value, Sized):
            if not isinstance(value, Iterable):
                return self
            exp = [exp if isinstance(exp, IExpression) else Variable(exp)
                   for exp in value if isinstance(exp, (IExpression, IType))]

        if len(exp) == 1:
            return StorageTryGetListMethod(StorageLocalGet())
        else:
            return self
