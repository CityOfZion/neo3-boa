from __future__ import annotations

import abc
from enum import IntEnum

from boa3.neo3.core import serialization, Size as s


class NodeCapabilityType(IntEnum):
    TCPSERVER = 0x01
    WSSERVER = 0x02
    FULLNODE = 0x10


class NodeCapability(serialization.ISerializable):
    """
    Capability base class.
    """

    def __init__(self, n_type: NodeCapabilityType = None):
        self.type = n_type

    def __len__(self):
        """ Get the total size in bytes of the object. """
        return s.uint8

    def __eq__(self, other):
        pass

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_uint8(self.type)
        self.serialize_without_type(writer)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.type = NodeCapabilityType(reader.read_uint8())
        self.deserialize_without_type(reader)

    @staticmethod
    def deserialize_from(reader: serialization.BinaryReader) -> NodeCapability:
        capability_type = NodeCapabilityType(reader.read_uint8())
        if capability_type in [NodeCapabilityType.TCPSERVER, NodeCapabilityType.WSSERVER]:
            capability = ServerCapability(capability_type)  # type: NodeCapability
        elif capability_type == NodeCapabilityType.FULLNODE:
            capability = FullNodeCapability()

        capability.deserialize_without_type(reader)
        return capability  # a type of Nodecapbility or inherited

    @abc.abstractmethod
    def deserialize_without_type(self, reader: serialization.BinaryReader) -> None:
        """ Deserialize from a buffer without reading the `type` member. """

    @abc.abstractmethod
    def serialize_without_type(self, writer: serialization.BinaryWriter) -> None:
        """ Serialize into a buffer without including the `type` member. """


class ServerCapability(NodeCapability):
    """
    A capability expressing node support for TCP or Websocket services.
    """

    def __init__(self, n_type: NodeCapabilityType = None, port: int = 0):
        super(ServerCapability, self).__init__(n_type)
        # None is allowed because that ensure we can still call `deserialize_from_bytes`
        if n_type and n_type not in [NodeCapabilityType.TCPSERVER, NodeCapabilityType.WSSERVER]:
            raise TypeError(f"{n_type} not one of: {NodeCapabilityType.TCPSERVER.name} {NodeCapabilityType.WSSERVER.name}")  # noqa
        self.port = port

    def __len__(self):
        return super(ServerCapability, self).__len__() + s.uint16

    def serialize_without_type(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream without serializing the base class `type` property.

        Args:
            writer: instance.
        """
        writer.write_uint16(self.port)

    def deserialize_without_type(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream without deserializing the base class `type` property.

        Args:
            reader: instance.
        """
        self.port = reader.read_uint16()


class FullNodeCapability(NodeCapability):
    """
    A capability expressing the node has full blockchain data and accepts relaying.
    """

    def __init__(self, start_height: int = 0):
        super(FullNodeCapability, self).__init__(NodeCapabilityType.FULLNODE)
        self.start_height = start_height

    def __len__(self):
        return super(FullNodeCapability, self).__len__() + s.uint32

    def serialize_without_type(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream without serializing the base class `type` property.

        Args:
            writer: instance.
        """
        writer.write_uint32(self.start_height)

    def deserialize_without_type(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream without deserializing the base class `type` property.

        Args:
            reader: instance.
        """
        self.start_height = reader.read_uint32()
