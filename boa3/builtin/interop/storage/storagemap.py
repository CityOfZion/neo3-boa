from typing import Union


class StorageMap:

    def __init__(self, context, prefix: Union[bytes, str]):
        from boa3.builtin.interop.storage.storagecontext import StorageContext

        self._context: StorageContext
        self._prefix: Union[bytes, str]

    def get(self, key: Union[str, bytes]) -> bytes:
        """
        Gets a value from the map based on the given key.

        :param key: value identifier in the store
        :type key: str or bytes
        :return: the value corresponding to given key for current storage context
        :rtype: bytes
        """
        pass

    def put(self, key: Union[str, bytes], value: Union[int, str, bytes]):
        """
        Inserts a given value in the key-value format into the map.

        :param key: the identifier in the store for the new value
        :type key: str or bytes
        :param value: value to be stored
        :type value: int or str or bytes
        """
        pass

    def delete(self, key: Union[str, bytes]):
        """
        Removes a given key from the map if exists.

        :param key: the identifier in the store for the new value
        :type key: str or bytes
        """
        pass
