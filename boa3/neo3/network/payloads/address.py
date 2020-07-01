from __future__ import annotations

from datetime import datetime
from enum import IntEnum
from typing import List, Optional

from netaddr import IPAddress  # type: ignore

from boa3.neo3.core import serialization, Size as s, utils
from boa3.neo3.network import capabilities
from boa3.neo3.network.payloads import VersionPayload


class AddressState(IntEnum):
    """
    Node state

    Used for tracking remote address state.
    """
    #: an address that has not been used before in the current connection cycle.
    NEW = 0x0

    #: an address that is associated with a live node and performing OK.
    CONNECTED = 0x1

    #: an address from a node that has been disconnected from due to
    #:
    #: - bad performance
    #: - malformed data or protocol responses
    #: - or max connections reached reasons.
    POOR = 0x2

    #: an address that could not be resolved or connected to due to a timeout.
    DEAD = 0x3


class DisconnectReason(IntEnum):
    """
    Reason for disconnecting a node.

    Will also be broadcasted back to the node when `this PR <https://github.com/neo-project/neo/pull/1154>`__ is merged.
    For now only used internally with logging.
    """
    UNKNOWN = 0x0
    MAX_CONNECTIONS_REACHED = 0x1
    POOR_PERFORMANCE = 0x2
    IPFILTER_NOT_ALLOWED = 0x3
    HANDSHAKE_VERSION_ERROR = 0x4
    HANDSHAKE_VERACK_ERROR = 0x5
    SHUTTING_DOWN = 0x6


class NetworkAddress(serialization.ISerializable):

    def __init__(self, address: str = None, timestamp: int = None,
                 capabilities: List[capabilities.NodeCapability] = None, state: AddressState = AddressState.NEW):
        """ Create an instance. """
        if timestamp is None:
            self.timestamp = int(datetime.utcnow().timestamp())
        else:
            self.timestamp = timestamp

        self.address = address if address else '0.0.0.0:0'  # host:port
        self.capabilities = capabilities if capabilities else []

        # none official properties
        self.state = state
        self.disconnect_reason = None  # type: Optional[DisconnectReason]
        self.last_connected = 0

    def __len__(self):
        """
        Get the total size in bytes of the object.

        Note:
            This size is only for the official properties such that it matches C#.
            Unofficial properties are not accounted for.
        """
        return s.uint32 + 16 + utils.get_var_size(self.capabilities)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.address == other.address
        else:
            return False

    def __repr__(self):
        return f"<{self.__class__.__name__} at {hex(id(self))}> {self.address} ({self.state.name})"

    def __str__(self):
        return self.address

    def __format__(self, format_spec):
        return self.address.__format__(format_spec)

    def __hash__(self):
        return hash((self.address, self.timestamp))

    @property
    def ip(self) -> str:
        host, port = self.address.split(":")
        return host

    @property
    def port(self) -> int:
        host, port = self.address.split(":")
        return int(port)

    @property
    def is_state_new(self) -> bool:
        return self.state == AddressState.NEW

    def set_state_new(self) -> None:
        self.state = AddressState.NEW

    @property
    def is_state_connected(self) -> bool:
        return self.state == AddressState.CONNECTED

    def set_state_connected(self) -> None:
        self.state = AddressState.CONNECTED

    @property
    def is_state_poor(self) -> bool:
        return self.state == AddressState.POOR

    def set_state_poor(self) -> None:
        self.state = AddressState.POOR

    @property
    def is_state_dead(self) -> bool:
        return self.state == AddressState.DEAD

    def set_state_dead(self) -> None:
        self.state = AddressState.DEAD

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_uint32(self.timestamp)
        ip = IPAddress(self.ip).ipv6()
        writer.write_bytes(ip.packed)
        writer.write_serializable_list(self.capabilities)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.timestamp = reader.read_uint32()

        full_address_bytes = bytearray(reader.read_bytes(16))
        ip_bytes = full_address_bytes[-4:]
        host = '.'.join(map(lambda b: str(b), ip_bytes))
        port = 0

        capabilities_cnt = reader.read_var_int(VersionPayload.MAX_CAPABILITIES)
        capabilities_list = []
        for _ in range(capabilities_cnt):
            capa = capabilities.NodeCapability.deserialize_from(reader)
            if isinstance(capa, capabilities.ServerCapability):
                port = capa.port
            capabilities_list.append(capa)
        self.capabilities = capabilities_list
        self.address = f"{host}:{port}"


class AddrPayload(serialization.ISerializable):
    def __init__(self, addresses: List[NetworkAddress] = None):
        """
        Should not be called directly. Use create() instead.
        """
        self.addresses = addresses if addresses else []

    def __len__(self):
        return utils.get_var_size(self.addresses)

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_var_int(len(self.addresses))
        for address in self.addresses:
            address.serialize(writer)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        addr_list_len = reader.read_var_int()
        for i in range(0, addr_list_len):
            nawt = NetworkAddress()
            nawt.deserialize(reader)
            self.addresses.append(nawt)

    @classmethod
    def create(cls, addresses: List[NetworkAddress]) -> AddrPayload:
        """
        Create payload.

        Args:
            addresses: network addresses
        """
        return cls(addresses)
