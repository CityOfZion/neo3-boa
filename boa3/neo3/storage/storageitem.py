from __future__ import annotations

from boa3.neo3.core import serialization, utils, IClonable


class StorageItem(serialization.ISerializable, IClonable):
    def __init__(self, value: bytes = None):
        self.value = value if value else b''

    def __len__(self):
        return utils.get_var_size(self.value)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.value == other.value

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        writer.write_var_bytes(self.value)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        self.value = reader.read_var_bytes()

    def clone(self) -> StorageItem:
        return StorageItem(self.value)

    def from_replica(self, replica: StorageItem) -> None:
        self.value = replica.value
