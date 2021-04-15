from typing import Union

from boa3.builtin.interop.storage.storagemap import StorageMap


class StorageContext:

    def __init__(self):
        pass

    def create_map(self, prefix: Union[str, bytes]) -> StorageMap:
        """
        Creates a storage map with the given prefix

        :param prefix: the identifier of the storage map
        :type prefix: str or bytes
        :return: a map with the key-values in the storage that match with the given prefix
        """
        pass
