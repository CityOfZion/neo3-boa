from boa3.internal.model.builtin.interop.storage.get.istoragegetmethod import IStorageGetMethod


class StorageGetBytesMethod(IStorageGetMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'get'
        value_type = Type.bytes

        super().__init__(identifier, value_type=value_type)

    def generate_default_value_opcodes(self, code_generator):
        # default_value = b''
        code_generator.convert_literal(b'')

    def generate_deserialize_value_opcodes(self, code_generator):
        # it doesn't need to deserialize bytes values
        return
