from boa3.internal.model.builtin.interop.storage.get.istoragegetmethod import IStorageGetMethod


class StorageGetUInt256Method(IStorageGetMethod):
    def __init__(self):
        from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type

        identifier = 'get_uint256'
        value_type = UInt256Type.build()

        super().__init__(identifier, value_type=value_type)

    def generate_default_value_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin

        code_generator.convert_literal(Builtin.UInt256.default_value)

    def generate_deserialize_value_opcodes(self, code_generator):
        # it doesn't need to deserialize bytes values
        return
