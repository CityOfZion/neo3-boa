__all__ = [
    'FindOptions',
    'StorageContext',
    'StorageMap',
    'get',
    'get_context',
    'get_read_only_context',
    'put',
    'delete',
    'find',
]


from typing import Union

from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.interop.storage.findoptions import FindOptions
from boa3.builtin.interop.storage.storagecontext import StorageContext
from boa3.builtin.interop.storage.storagemap import StorageMap


def get_context() -> StorageContext:
    """
    Gets current storage context.

    >>> get_context()       # StorageContext cannot be read outside the blockchain
    _InteropInterface

    :return: the current storage context
    :rtype: StorageContext
    """
    pass


def get(key: bytes, context: StorageContext = get_context()) -> bytes:
    """
    Gets a value from the persistent store based on the given key.

    >>> put(b'unit', 'test')
    ... get(b'unit')
    'test'

    >>> get(b'fake_key')
    ''

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context
    :rtype: bytes
    """
    pass


def get_read_only_context() -> StorageContext:
    """
    Gets current read only storage context.

    >>> get_context()       # StorageContext cannot be read outside the blockchain
    _InteropInterface

    :return: the current read only storage context
    :rtype: StorageContext
    """
    pass


def put(key: bytes, value: Union[int, bytes, str], context: StorageContext = get_context()):
    """
    Inserts a given value in the key-value format into the persistent storage.

    >>> put(b'unit', 'test')
    None

    :param key: the identifier in the store for the new value
    :type key: bytes
    :param value: value to be stored
    :type value: int or str or bytes
    :param context: storage context to be used
    :type context: StorageContext
    """
    pass


def delete(key: bytes, context: StorageContext = get_context()):
    """
    Removes a given key from the persistent storage if exists.

    >>> put(b'unit', 'test')
    ... delete()
    ... get(b'unit')
    ''

    :param key: the identifier in the store for the new value
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    """
    pass


def find(prefix: bytes,
         context: StorageContext = get_context(),
         options: FindOptions = FindOptions.NONE) -> Iterator:
    """
    Searches in the storage for keys that start with the given prefix.

    >>> put(b'a1', 'one')
    ... put(b'a2', 'two')
    ... put(b'a3', 'three')
    ... put(b'b4', 'four')
    ... findIterator = find(b'a')
    ... findResults = []
    ... while findIterator.next():
    ...     findResults.append(findIterator.value)
    ... findResults
    ['one', 'two', 'three']

    :param prefix: prefix to find the storage keys
    :type prefix: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :param options: the options of the search
    :type options: FindOptions
    :return: an iterator with the search results
    :rtype: Iterator
    """
    pass
