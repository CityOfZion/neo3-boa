from boa3.internal.model.builtin.interop.storage.put.istorageputmethod import IStoragePutMethod


class StoragePutUInt256Method(IStoragePutMethod):
    def __init__(self):
        from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type

        identifier = 'put_uint256'
        value_type = UInt256Type.build()

        super().__init__(identifier, value_type=value_type)

    def generate_serialize_value_opcodes(self, code_generator):
        # it doesn't need to serialize UInt256 because it is also bytes value
        return
