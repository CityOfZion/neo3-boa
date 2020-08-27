from __future__ import annotations

from enum import IntEnum, IntFlag

import lz4.block  # type: ignore

from boa3.neo3 import network_logger as logger
from boa3.neo3.core import Size as s, serialization
from boa3.neo3.network import payloads


class MessageType(IntEnum):
    VERSION = 0x00
    VERACK = 0x01

    GETADDR = 0x10
    ADDR = 0x11
    PING = 0x18
    PONG = 0x19

    GETHEADERS = 0x20
    HEADERS = 0x21
    GETBLOCKS = 0x24
    MEMPOOL = 0x25
    INV = 0x27
    GETDATA = 0x28
    GETBLOCKDATA = 0x29
    NOTFOUND = 0x2a
    TRANSACTION = 0x2b
    BLOCK = 0x2c
    CONSENSUS = 0x2d
    REJECT = 0x2f

    FILTERLOAD = 0x30
    FILTERADD = 0x31
    FILTERCLEAR = 0x32
    MERKLEBLOCK = 0x38

    ALERT = 0x40

    DEFAULT = 0xFF  # not supported in the real protocol


class MessageConfig(IntFlag):
    NONE = 0
    COMPRESSED = 1 << 0


class Message(serialization.ISerializable):
    PAYLOAD_MAX_SIZE = 0x2000000
    COMPRESSION_MIN_SIZE = 128
    COMPRESSION_THRESHOLD = 64

    def __init__(self, msg_type: MessageType = None, payload: serialization.ISerializable_T = None):
        """

        Args:
            msg_type: message object configuration.
            payload: an identifier specifying the purpose of the message.
        """
        self.config = MessageConfig.NONE  #: MessageConfig: message object configuration.
        # something strange is going on if the check does not explicitly include "is not None", then it will
        # use the 'else' result even if a msg_type is clearly specified and present in the debugger
        #: MessageType: an identifier specifying the purpose of the message.
        self.type: MessageType = msg_type if msg_type is not None else MessageType.DEFAULT
        self.payload: serialization.ISerializable_T = payloads.EmptyPayload()  # type: ignore
        # mypy doesn't get EmptyPayload is an ISerializable

        if payload:
            self.payload = payload

    def __len__(self):
        """ Get the total size in bytes of the object. """
        return s.uint8 + s.uint8 + len(self.payload)

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        payload = self.payload.to_array()

        if len(self.payload) > self.COMPRESSION_MIN_SIZE and MessageConfig.COMPRESSED not in self.config:
            compressed_data = lz4.block.compress(self.payload.to_array(), store_size=False)
            if len(compressed_data) < len(self.payload) - self.COMPRESSION_THRESHOLD:
                payload = compressed_data
                self.config |= MessageConfig.COMPRESSED

        writer.write_uint8(self.config)
        writer.write_uint8(self.type.value)
        writer.write_var_bytes(payload)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.config = MessageConfig(reader.read_uint8())
        x = reader.read_uint8()
        self.type = MessageType(x)
        # self.type = MessageType(reader.read_uint8())

        payload_data = reader.read_var_bytes(self.PAYLOAD_MAX_SIZE)
        if len(payload_data) > 0:
            if MessageConfig.COMPRESSED in self.config:
                # From the lz4 documentation:
                # "The uncompressed_size argument specifies an upper bound on the size of the uncompressed data size
                # rather than an absolute value"
                try:
                    payload_data = lz4.block.decompress(payload_data, uncompressed_size=self.PAYLOAD_MAX_SIZE)
                except lz4.block.LZ4BlockError:
                    raise ValueError("Invalid payload data - decompress failed")

            self.payload = self._payload_from_data(self.type, payload_data)

        if self.payload is None:
            self.payload = payloads.EmptyPayload()

    @staticmethod
    def _payload_from_data(msg_type, data):
        with serialization.BinaryReader(data) as br:
            if msg_type in [MessageType.INV, MessageType.GETDATA]:
                return br.read_serializable(payloads.InventoryPayload)
            elif msg_type == MessageType.GETBLOCKDATA:
                return br.read_serializable(payloads.GetBlockDataPayload)
            elif msg_type == MessageType.VERSION:
                return br.read_serializable(payloads.VersionPayload)
            elif msg_type == MessageType.VERACK:
                return br.read_serializable(payloads.EmptyPayload)
            elif msg_type == MessageType.BLOCK:
                return br.read_serializable(payloads.Block)
            elif msg_type == MessageType.HEADERS:
                return br.read_serializable(payloads.HeadersPayload)
            elif msg_type in [MessageType.PING, MessageType.PONG]:
                return br.read_serializable(payloads.PingPayload)
            elif msg_type == MessageType.ADDR:
                return br.read_serializable(payloads.AddrPayload)
            elif msg_type == MessageType.TRANSACTION:
                return br.read_serializable(payloads.Transaction)
            else:
                logger.debug(f"Unsupported payload {msg_type.name}")
