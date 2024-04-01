from boa3.internal.model.builtin.interop.storage.put.istorageputmethod import IStoragePutMethod


class StoragePutUInt160Method(IStoragePutMethod):
    def __init__(self):
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'put_uint160'
        value_type = UInt160Type.build()

        super().__init__(identifier, value_type=value_type)

    def generate_serialize_value_opcodes(self, code_generator):
        # it doesn't need to serialize UInt160 because it is also bytes value
        return
