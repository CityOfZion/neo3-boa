from boa3.internal.model.builtin.interop.storage.put.istorageputmethod import IStoragePutMethod


class StoragePutDictMethod(IStoragePutMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'put_dict'
        value_type = Type.dict

        super().__init__(identifier, value_type=value_type)

    def generate_serialize_value_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.interop import Interop

        converter = Interop.Serialize
        code_generator.convert_builtin_method_call(converter, is_internal=True)
