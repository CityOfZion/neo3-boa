from typing import Union

from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.interop.storage.storagecontext import StorageContext


def get(key: Union[str, bytes]) -> bytes:
    """
    Gets a value from the persistent store based on the given key.

    :param key: value identifier in the store
    :type key: str or bytes
    :return: the value corresponding to given key for current storage context
    :rtype: bytes
    """
    pass


def get_context() -> StorageContext:
    """
    Gets current storage context

    :return: the current storage context
    :rtype: StorageContext
    """
    pass


def put(key: Union[str, bytes], value: Union[int, str, bytes]):
    """
    Inserts a given value in the key-value format into the persistent storage.

    :param key: the identifier in the store for the new value
    :type key: str or bytes
    :param value: value to be stored
    :type value: int or str or bytes
    """
    pass


def delete(key: Union[str, bytes]):
    """
    Removes a given key from the persistent storage if exists.

    :param key: the identifier in the store for the new value
    :type key: str or bytes
    """
    pass


def find(prefix: Union[str, bytes]) -> Iterator:
    """
    Searches in the storage for keys that start with the given prefix

    :param prefix: prefix to find the storage keys
    :type prefix: str or bytes
    :return: an iterator with the search results
    :rtype: Iterator
    """
    pass
