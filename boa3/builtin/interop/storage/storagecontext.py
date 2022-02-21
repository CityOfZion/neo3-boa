from __future__ import annotations

from boa3.builtin.interop.storage.storagemap import StorageMap
from boa3.builtin.type import ByteString


class StorageContext:
    """
    The storage context used to read and write data in smart contracts.
    """

    def __init__(self):
        pass

    def create_map(self, prefix: ByteString) -> StorageMap:
        """
        Creates a storage map with the given prefix.

        :param prefix: the identifier of the storage map
        :type prefix: str or bytes
        :return: a map with the key-values in the storage that match with the given prefix
        :rtype: StorageMap
        """
        pass

    def as_read_only(self) -> StorageContext:
        """
        Converts the specified storage context to a new readonly storage context.

        :return: current StorageContext as ReadOnly
        :rtype: StorageContext
        """
        pass
