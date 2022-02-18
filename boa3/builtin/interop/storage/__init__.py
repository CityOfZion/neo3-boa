from typing import Union

from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.interop.storage.findoptions import FindOptions
from boa3.builtin.interop.storage.storagecontext import StorageContext
from boa3.builtin.interop.storage.storagemap import StorageMap
from boa3.builtin.type import ByteString


def get(key: ByteString, context: StorageContext = None) -> bytes:
    """
    Gets a value from the persistent store based on the given key.

    :param key: value identifier in the store
    :type key: str or bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context
    :rtype: bytes
    """
    pass


def get_context() -> StorageContext:
    """
    Gets current storage context.

    :return: the current storage context
    :rtype: StorageContext
    """
    pass


def get_read_only_context() -> StorageContext:
    """
    Gets current read only storage context.

    :return: the current read only storage context
    :rtype: StorageContext
    """
    pass


def put(key: ByteString, value: Union[int, ByteString], context: StorageContext = None):
    """
    Inserts a given value in the key-value format into the persistent storage.

    :param key: the identifier in the store for the new value
    :type key: str or bytes
    :param value: value to be stored
    :type value: int or str or bytes
    :param context: storage context to be used
    :type context: StorageContext
    """
    pass


def delete(key: ByteString, context: StorageContext = None):
    """
    Removes a given key from the persistent storage if exists.

    :param key: the identifier in the store for the new value
    :type key: str or bytes
    :param context: storage context to be used
    :type context: StorageContext
    """
    pass


def find(prefix: ByteString,
         context: StorageContext = None,
         options: FindOptions = FindOptions.NONE) -> Iterator:
    """
    Searches in the storage for keys that start with the given prefix.

    :param prefix: prefix to find the storage keys
    :type prefix: str or bytes
    :param context: storage context to be used
    :type context: StorageContext
    :param options: the options of the search
    :type options: FindOptions
    :return: an iterator with the search results
    :rtype: Iterator
    """
    pass
