from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable


class StorageContextCreateMapMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontexttype import _StorageContext
        from boa3.internal.model.builtin.interop.storage.storagemap.storagemaptype import _StorageMap
        from boa3.internal.model.type.type import Type

        identifier = 'create_map'
        byte_string_type = Type.bytes

        args: dict[str, Variable] = {'self': Variable(_StorageContext),
                                     'prefix': Variable(byte_string_type)}

        super().__init__(identifier, args, return_type=_StorageMap)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.storage.storagemap.storagemaptype import _StorageMap as StorageMapType
        code_generator.convert_builtin_method_call(StorageMapType.constructor_method(), is_internal=True)
