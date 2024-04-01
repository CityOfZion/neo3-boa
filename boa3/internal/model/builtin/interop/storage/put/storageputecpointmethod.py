from boa3.internal.model.builtin.interop.storage.put.istorageputmethod import IStoragePutMethod


class StoragePutECPointMethod(IStoragePutMethod):
    def __init__(self):
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType

        identifier = 'put_ecpoint'
        value_type = ECPointType.build()

        super().__init__(identifier, value_type=value_type)

    def generate_serialize_value_opcodes(self, code_generator):
        # it doesn't need to serialize ECPoint because it is also bytes value
        return
