from boa3.internal.model.builtin.interop.storage.get.istoragegetmethod import IStorageGetMethod


class StorageGetIntMethod(IStorageGetMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'get_int'
        value_type = Type.int

        super().__init__(identifier, value_type=value_type)

    def generate_default_value_opcodes(self, code_generator):
        # default_value = 0
        code_generator.convert_literal(0)

    def generate_deserialize_value_opcodes(self, code_generator):
        from boa3.internal.model.builtin.method.tointmethod import ToInt
        from boa3.internal.model.type.type import Type

        converter = ToInt.build(Type.bytes)
        code_generator.convert_builtin_method_call(converter)
