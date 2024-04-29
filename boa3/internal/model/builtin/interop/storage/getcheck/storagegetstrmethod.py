from boa3.internal.model.builtin.interop.storage.getcheck.istoragetrygetmethod import IStorageTryGetMethod


class StorageTryGetStrMethod(IStorageTryGetMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'try_get_str'
        value_type = Type.str

        super().__init__(identifier, value_type=value_type)

    def generate_default_value_opcodes(self, code_generator):
        # default_value = ''
        code_generator.convert_literal('')

    def generate_deserialize_value_opcodes(self, code_generator):
        from boa3.internal.model.builtin.method.tostrmethod import ToStr
        from boa3.internal.model.type.type import Type

        converter = ToStr.build(Type.bytes)
        code_generator.convert_builtin_method_call(converter)
