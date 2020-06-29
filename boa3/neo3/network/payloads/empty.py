from boa3.neo3.core import serialization


class EmptyPayload(serialization.ISerializable):
    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """ we don't have to do anything, because it should stay empty. """

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """ we don't have to do anything, because it has no attributes. """

    def __len__(self):
        return 0
