from __future__ import annotations

import datetime
import random
from typing import List, Type

from boa3.neo3 import settings
from boa3.neo3.core import Size as s, serialization, utils
from boa3.neo3.network import capabilities


class VersionPayload(serialization.ISerializable):
    """
    A payload carrying node handshake data.
    """
    MAX_CAPABILITIES = 32

    def __init__(self, nonce: int = None, user_agent: str = None,
                 capabilities: List[capabilities.NodeCapability] = None):
        """
        Should not be called directly. Use create() instead.
        """

        #: A network id. Differs for NEO's Mainnet (use 5195086) and Testnet (use 1951352142).
        #:
        #: Reference nodes will disconnect if the value doesn't match with their local settings.
        self.magic = settings.network.magic
        self.version = 0
        self.timestamp = int(datetime.datetime.utcnow().timestamp())
        #: A unique identifier for the node.
        self.nonce = nonce if nonce else random.randint(0, 10000)
        #: A node client description i.e. "NEO-PYTHON-V001"
        self.user_agent = user_agent if user_agent else ""
        #: A list of services a node offers. See :ref:`capabilities <library-network-capabilities>`
        self.capabilities = capabilities if capabilities else []

    def __len__(self):
        """ Get the total size in bytes of the object. """
        return s.uint32 + s.uint32 + s.uint32 + s.uint32 + utils.get_var_size(self.user_agent) + \
            utils.get_var_size(self.capabilities)

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_uint32(self.magic)
        writer.write_uint32(self.version)
        writer.write_uint32(self.timestamp)
        writer.write_uint32(self.nonce)
        writer.write_var_string(self.user_agent)
        writer.write_serializable_list(self.capabilities)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.magic = reader.read_uint32()
        self.version = reader.read_uint32()
        self.timestamp = reader.read_uint32()
        self.nonce = reader.read_uint32()
        self.user_agent = reader.read_var_string(max=1024)

        capabilities_cnt = reader.read_var_int(self.MAX_CAPABILITIES)
        capabilities_list = []
        for _ in range(capabilities_cnt):
            capabilities_list.append(capabilities.NodeCapability.deserialize_from(reader))
        self.capabilities = capabilities_list

    @classmethod
    def deserialize_from_bytes(cls: Type[VersionPayload], data: bytes) -> VersionPayload:
        """ Deserialize object. """
        with serialization.BinaryReader(data) as br:
            obj = cls()
            obj.deserialize(br)
            return obj

    @staticmethod
    def create(nonce: int, user_agent: str, capabilities: List[capabilities.NodeCapability]) -> VersionPayload:
        """
        Create payload.

        Args:
            nonce: unique number which identifies the node instance.
            user_agent: node user agent description. e.g. "NEO3-PYTHON-V001". Max 1024 bytes.
            capabilities: a list of services a node offers.
        """
        return VersionPayload(nonce, user_agent, capabilities)
