__all__ = ['StorageMap']


class StorageMap:
    """
    The key-value storage for the specific prefix in the given storage context.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/services/StorageMap>`__
    to learn more about StorageMap.
    """

    def __init__(self, context, prefix: bytes):
        from boa3.builtin.interop.storage import StorageContext

        self._context: StorageContext
        self._prefix: bytes

    def get(self, key: bytes) -> bytes:
        """
        Gets a value from the map based on the given key.

        :param key: value identifier in the store
        :type key: bytes
        :return: the value corresponding to given key for current storage context
        :rtype: bytes
        """
        pass

    def put(self, key: bytes, value: int | bytes | str):
        """
        Inserts a given value in the key-value format into the map.

        :param key: the identifier in the store for the new value
        :type key: bytes
        :param value: value to be stored
        :type value: int or str or bytes
        """
        pass

    def delete(self, key: bytes):
        """
        Removes a given key from the map if exists.

        :param key: the identifier in the store for the new value
        :type key: bytes
        """
        pass
