__all__ = [
    'FindOptions',
    'StorageContext',
    'StorageMap',
    'get',
    'get_int',
    'get_bool',
    'get_str',
    'get_uint160',
    'get_uint256',
    'get_ecpoint',
    'get_context',
    'get_read_only_context',
    'put',
    'put_int',
    'put_bool',
    'put_str',
    'put_uint160',
    'put_uint256',
    'put_ecpoint',
    'delete',
    'find',
]

from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.interop.storage.findoptions import FindOptions
from boa3.builtin.interop.storage.storagecontext import StorageContext
from boa3.builtin.interop.storage.storagemap import StorageMap
from boa3.builtin.type import UInt160, UInt256, ECPoint


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
    b'test'

    >>> get(b'fake_key')
    b''

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context
    :rtype: bytes
    """
    pass


def get_int(key: bytes, context: StorageContext = get_context()) -> int:
    """
    Gets a value as integer from the persistent store based on the given key.
    It's equivalent to boa3.builtin.type.helper.to_int(get(key, context))

    >>> put_int(b'unit', 5)
    ... get_int(b'unit')
    5

    >>> get_int(b'fake_key')
    0

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context
    :rtype: int
    """
    pass


def get_bool(key: bytes, context: StorageContext = get_context()) -> bool:
    """
    Gets a value as boolean from the persistent store based on the given key.
    It's equivalent to boa3.builtin.type.helper.to_bool(get(key, context))

    >>> put_bool(b'unit', True)
    ... get_bool(b'unit')
    True

    >>> get_bool(b'fake_key')
    False

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context
    :rtype: bool
    """
    pass


def get_str(key: bytes, context: StorageContext = get_context()) -> str:
    """
    Gets a value as string from the persistent store based on the given key.
    It's equivalent to boa3.builtin.type.helper.to_str(get(key, context))

    >>> put_str(b'unit', 'test')
    ... get_str(b'unit')
    'test'

    >>> get_str(b'fake_key')
    ''

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context
    :rtype: str
    """
    pass


def get_uint160(key: bytes, context: StorageContext = get_context()) -> UInt160:
    """
    Gets a value as UInt160 from the persistent store based on the given key.
    It's equivalent UInt160(get(key, context))

    >>> put_uint160(b'unit', UInt160(b'0123456789ABCDEFGHIJ'))
    ... get_uint160(b'unit')
    UInt160(0x4a49484746454443424139383736353433323130)

    >>> get_uint160(b'fake_key')
    UInt160(0x0000000000000000000000000000000000000000)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context
    :rtype: UInt160
    """
    pass


def get_uint256(key: bytes, context: StorageContext = get_context()) -> UInt256:
    """
    Gets a value as UInt256 from the persistent store based on the given key.
    It's equivalent UInt256(get(key, context))

    >>> put_uint256(b'unit', UInt256(b'0123456789ABCDEFGHIJKLMNOPQRSTUV'))
    ... get_uint256(b'unit')
    UInt256(0x565554535251504f4e4d4c4b4a49484746454443424139383736353433323130)

    >>> get_uint160(b'fake_key')
    UInt256(0x0000000000000000000000000000000000000000000000000000000000000000)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context
    :rtype: UInt256
    """
    pass


def get_ecpoint(key: bytes, context: StorageContext = get_context()) -> ECPoint:
    """
    Gets a value as ECPoint from the persistent store based on the given key.
    It's equivalent ECPoint(get(key, context))

    >>> put_ecpoint(b'unit', ECPoint(b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'))
    ... get_ecpoint(b'unit')
    ECPoint(0x57565554535251504f4e4d4c4b4a49484746454443424139383736353433323130)

    >>> get_ecpoint(b'fake_key')
    ECPoint(0x000000000000000000000000000000000000000000000000000000000000000000)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context
    :rtype: ECPoint
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


def put(key: bytes, value: bytes, context: StorageContext = get_context()):
    """
    Inserts a given bytes value in the key-value format into the persistent storage.

    >>> put(b'unit', b'test')
    None

    :param key: the identifier in the store for the new value
    :type key: bytes
    :param value: value to be stored
    :type value: bytes
    :param context: storage context to be used
    :type context: StorageContext
    """
    pass


def put_int(key: bytes, value: int, context: StorageContext = get_context()):
    """
    Inserts a given integer value in the key-value format into the persistent storage.
    It's equivalent to put(key, boa3.builtin.type.helper.to_int(value), context)

    >>> put_int(b'unit', 5)
    None

    :param key: the identifier in the store for the new value
    :type key: bytes
    :param value: value to be stored
    :type value: int
    :param context: storage context to be used
    :type context: StorageContext
    """
    pass


def put_bool(key: bytes, value: bool, context: StorageContext = get_context()):
    """
    Inserts a given boolean value in the key-value format into the persistent storage.
    It's equivalent to put(key, boa3.builtin.type.helper.to_bool(value), context)

    >>> put_bool(b'unit', True)
    None

    :param key: the identifier in the store for the new value
    :type key: bytes
    :param value: value to be stored
    :type value: bool
    :param context: storage context to be used
    :type context: StorageContext
    """
    pass


def put_str(key: bytes, value: str, context: StorageContext = get_context()):
    """
    Inserts a given str value in the key-value format into the persistent storage.
    It's equivalent to put(key, boa3.builtin.type.helper.to_str(value), context)

    >>> put_str(b'unit', 'test')
    None

    :param key: the identifier in the store for the new value
    :type key: bytes
    :param value: value to be stored
    :type value: str
    :param context: storage context to be used
    :type context: StorageContext
    """
    pass


def put_uint160(key: bytes, value: UInt160, context: StorageContext = get_context()):
    """
    Inserts a given UInt160 value in the key-value format into the persistent storage.
    It's equivalent to put(key, value, context) since UInt160 is a subclass of bytes

    >>> put_uint160(b'unit', UInt160(b'0123456789ABCDEFGHIJ'))
    None

    :param key: the identifier in the store for the new value
    :type key: bytes
    :param value: value to be stored
    :type value: UInt160
    :param context: storage context to be used
    :type context: StorageContext
    """
    pass


def put_uint256(key: bytes, value: UInt256, context: StorageContext = get_context()):
    """
    Inserts a given UInt256 value in the key-value format into the persistent storage.
    It's equivalent to put(key, value, context) since UInt256 is a subclass of bytes

    >>> put_uint256(b'unit', UInt256(b'0123456789ABCDEFGHIJKLMNOPQRSTUV'))
    None

    :param key: the identifier in the store for the new value
    :type key: bytes
    :param value: value to be stored
    :type value: UInt256
    :param context: storage context to be used
    :type context: StorageContext
    """
    pass


def put_ecpoint(key: bytes, value: ECPoint, context: StorageContext = get_context()):
    """
    Inserts a given ECPoint value in the key-value format into the persistent storage.
    It's equivalent to put(key, value, context) since ECPoint is a subclass of bytes

    >>> put_ecpoint(b'unit', ECPoint(b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'))
    None

    :param key: the identifier in the store for the new value
    :type key: bytes
    :param value: value to be stored
    :type value: ECPoint
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
