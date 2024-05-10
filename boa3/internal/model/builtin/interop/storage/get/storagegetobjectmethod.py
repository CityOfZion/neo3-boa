from boa3.internal.model.builtin.interop.storage.get.istoragegetmethod import IStorageGetMethod


class StorageGetObjectMethod(IStorageGetMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'get_object'
        value_type = Type.any

        super().__init__(identifier, value_type=value_type)

    def generate_default_value_opcodes(self, code_generator):
        from boa3.internal.model.type.type import Type
        # default_value = object()
        code_generator.convert_new_empty_array(0, Type.list, as_struct=True)

    def generate_deserialize_value_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.interop import Interop

        converter = Interop.Deserialize
        code_generator.convert_builtin_method_call(converter, is_internal=True)
