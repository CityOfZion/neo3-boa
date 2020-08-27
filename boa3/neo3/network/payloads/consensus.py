from __future__ import annotations

import hashlib
from enum import IntEnum
from typing import TypeVar

from boa3.neo3.core import Size as s, serialization, utils, types
from boa3.neo3.network import payloads

ConsensusMessage_t = TypeVar('ConsensusMessage_t', bound='ConsensusMessage')


class ConsensusMessageType(IntEnum):
    CHANGE_VIEW = 0x00,
    PREPARE_REQUEST = 0x20,
    PREPARE_RESPONSE = 0x21,
    COMMIT = 0x30,
    RECOVERY_REQUEST = 0x40,
    RECOVERY_MESSAGE = 0x41


class ConsensusMessage(serialization.ISerializable):
    """
    Base class for the various consensus messages
    """

    def __init__(self, type: ConsensusMessageType = None):
        self.type = type if type else ConsensusMessageType.CHANGE_VIEW
        self.view_number: int = 0

    def __len__(self):
        return s.uint8 + s.uint8

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_uint8(self.type)
        writer.write_uint8(self.view_number)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.type = ConsensusMessageType(reader.read_uint8())
        self.view_number = reader.read_uint8()

    def deserialize_specialization_from_bytes(self, data: bytearray) -> ConsensusMessage_t:
        # TODO: not implemented. Requires all ConsensusMessage subclasses to be implemented. Low priority.
        pass


class ConsensusPayload(serialization.ISerializable, payloads.IInventory):
    def __init__(self, version: int = 0,
                 prev_hash: types.UInt256 = None,
                 block_index: int = 0,
                 validator_index: int = 0,
                 data: bytes = None,
                 witness: payloads.Witness = None):
        self.version = version
        self.prev_hash = prev_hash if prev_hash else types.UInt256.zero()
        self.block_index = block_index
        self.validator_index = validator_index
        self.data = data if data else b''
        self.witness = witness if witness else payloads.Witness()

    def __len__(self):
        return (s.uint32 + len(self.prev_hash) + s.uint32 + s.uint16 + utils.get_var_size(self.data) + 1
                + len(self.witness))

    def hash(self) -> types.UInt256:
        with serialization.BinaryWriter() as bw:
            self.serialize_unsigned(bw)
            data_to_hash = bytearray(bw._stream.getvalue())
            data = hashlib.sha256(hashlib.sha256(data_to_hash).digest()).digest()
            return types.UInt256(data=data)

    @property
    def inventory_type(self):
        return payloads.InventoryType.CONSENSUS

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        self.serialize_unsigned(writer)
        writer.write_uint8(1)
        writer.write_serializable(self.witness)

    def serialize_unsigned(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream excluding the validation byte + witness.

        Args:
            writer: instance.
        """
        writer.write_uint32(self.version)
        writer.write_serializable(self.prev_hash)
        writer.write_uint32(self.block_index)
        writer.write_uint16(self.validator_index)
        writer.write_var_bytes(self.data)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.

        Raises:
            ValueError: if the validation byte is not 1
        """
        self.deserialize_unsigned(reader)
        if reader.read_uint8() != 1:
            raise ValueError("Deserialization error - validation byte not 1")
        self.witness = reader.read_serializable(payloads.Witness)

    def deserialize_unsigned(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream excluding the validation byte + witness.

        Args:
            reader: instance.
        """
        self.version = reader.read_uint32()
        self.prev_hash = reader.read_serializable(types.UInt256)
        self.block_index = reader.read_uint32()
        self.validator_index = reader.read_uint16()
        self.data = reader.read_var_bytes()

    @classmethod
    def create(cls, version: int, prev_hash: types.UInt256, block_index: int, validator_index: int, data: bytes,
               witness: payloads.Witness) -> ConsensusPayload:
        return cls(version, prev_hash, block_index, validator_index, data, witness)


class ConsensusData(serialization.ISerializable):
    def __init__(self, primary_index: int = 0, nonce: int = 0):
        self.primary_index = primary_index
        self.nonce = nonce

    def __len__(self):
        return utils.get_var_size(self.primary_index) + s.uint64

    def hash(self) -> types.UInt256:
        data = hashlib.sha256(hashlib.sha256(self.to_array()).digest()).digest()
        return types.UInt256(data=data)

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_var_int(self.primary_index)
        writer.write_uint64(self.nonce)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.primary_index = reader.read_var_int(max=1024)  # comes from C#'s Clockchain.MaxValidators
        self.nonce = reader.read_uint64()
