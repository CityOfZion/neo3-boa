from boa3.internal.model.builtin.interop.storage.put.istorageputmethod import IStoragePutMethod


class StoragePutIntMethod(IStoragePutMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'put_int'
        value_type = Type.int

        super().__init__(identifier, value_type=value_type)

    def generate_serialize_value_opcodes(self, code_generator):
        # it doesn't need to serialize primitive types values on put
        return
