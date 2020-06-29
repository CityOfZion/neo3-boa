from __future__ import annotations

from boa3.neo3.core import serialization, utils, Size as s, cryptography as crypto


class FilterAddPayload(serialization.ISerializable):
    def __init__(self, data: bytes = None):
        """
        Should not be called directly. Use create() instead.
        """
        self.data = data if data else b''

    def __len__(self):
        return utils.get_var_size(self.data)

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_var_bytes(self.data)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.data = reader.read_var_bytes(520)

    @classmethod
    def create(cls, data: bytes) -> FilterAddPayload:
        """
        Create payload.

        Args:
            data: the data to add to the configured bloomfilter.
        """
        return cls(data)


class FilterLoadPayload(serialization.ISerializable):
    def __init__(self, filter: bytes = None, K: int = 0, tweak: int = 0):
        """
        Should not be called directly. Use create() instead.
        """
        self.filter = filter if filter else b''
        self.K = K
        self.tweak = tweak

    def __len__(self):
        return utils.get_var_size(self.filter) + s.uint8 + s.uint32

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_var_bytes(self.filter)
        writer.write_uint8(self.K)
        writer.write_uint32(self.tweak)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.filter = reader.read_var_bytes(max=36000)
        self.K = reader.read_uint8()
        if self.K > 50:
            raise ValueError("Deserialization error - K exceeds limit of 50")
        self.tweak = reader.read_uint32()

    @classmethod
    def create(cls, filter: crypto.BloomFilter) -> FilterLoadPayload:
        """
        Create payload.

        Args:
            filter: bloom filter to load
        """
        return cls(filter=filter.get_bits(), K=filter.K, tweak=filter.tweak)
