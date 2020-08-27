from __future__ import annotations

import abc
from enum import IntEnum
from typing import List

from boa3.neo3.core import Size as s, utils
from boa3.neo3.core import serialization
from boa3.neo3.core import types


class InventoryType(IntEnum):
    TX = 0x2b
    BLOCK = 0x2c
    CONSENSUS = 0x2d


class InventoryPayload(serialization.ISerializable):
    """
    A payload used to share inventory hashes.

    See also:
        - :ref:`getblocks <message-usage-getblocks>`
        - :ref:`getdata <message-usage-getdata>`
        - :ref:`mempool <message-usage-mempool>`
    """

    def __init__(self, type: InventoryType = None, hashes: List[types.UInt256] = None):
        """
        Should not be called directly. Use create() instead.
        """
        self.type = type
        self.hashes = hashes if hashes else []

    def __len__(self):
        """ Get the total size in bytes of the object. """
        return s.uint8 + utils.get_var_size(self.hashes)

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_uint8(self.type)
        writer.write_var_int(len(self.hashes))
        for h in self.hashes:  # type: types.UInt256
            writer.write_bytes(h.to_array())

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.type = InventoryType(reader.read_uint8())
        self.hashes = reader.read_serializable_list(types.UInt256)

    @classmethod
    def create(cls, type: InventoryType, hashes: List[types.UInt256]) -> InventoryPayload:
        """
        Create payload.

        Args:
            type: indicator to what type of object the the hashes of this payload relate to.
            hashes: hashes of "type" objects.
        """
        return cls(type, hashes)


class IInventory(abc.ABC):
    @abc.abstractmethod
    def hash(self) -> types.UInt256:
        """"""

    @property
    @abc.abstractmethod
    def inventory_type(self) -> InventoryType:
        """"""
