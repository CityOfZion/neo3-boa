from typing import Any


def get(key: Any) -> bytes:
    """
    Gets a value from the persistent store based on the given key.

    :param key: value identifier in the store
    :type key: str or bytes
    :return: the value corresponding to given key for current storage context
    :rtype: bytes
    """
    pass


def put(key: Any, value: Any):
    """
    Inserts a given value in the key-value format into the persistent storage.

    :param key: the identifier in the store for the new value
    :type key: str or bytes
    :param value: value to be stored
    :type value: int or str or bytes
    """
    pass


def delete(key: Any):
    """
    Removes a given key from the persistent storage if exists.

    :param key: the identifier in the store for the new value
    :type key: str or bytes
    """
    pass
