__all__ = [
    'StorageContext',
    'StorageMap',
    'get',
    'get_int',
    'get_bool',
    'get_str',
    'get_list',
    'get_dict',
    'get_object',
    'get_uint160',
    'get_uint256',
    'get_ecpoint',
    'try_get',
    'try_get_int',
    'try_get_bool',
    'try_get_str',
    'try_get_list',
    'try_get_dict',
    'try_get_object',
    'try_get_uint160',
    'try_get_uint256',
    'try_get_ecpoint',
    'get_context',
    'get_read_only_context',
    'put',
    'put_int',
    'put_bool',
    'put_str',
    'put_list',
    'put_dict',
    'put_object',
    'put_uint160',
    'put_uint256',
    'put_ecpoint',
    'delete',
    'find',
]

from typing import Any

from boa3.sc.storage.storagecontext import StorageContext
from boa3.sc.storage.storagemap import StorageMap
from boa3.sc.types import FindOptions, UInt256, ECPoint, UInt160
from boa3.sc.utils.iterator import Iterator


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

    >>> put(b'unit', b'test')
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


def try_get(key: bytes, context: StorageContext = get_context()) -> tuple[bytes, bool]:
    """
    Gets a value from the persistent store based on the given key and returns whether the value is stored.

    >>> put(b'unit', b'test')
    ... try_get(b'unit')
    (b'test', True)

    >>> try_get(b'fake_key')
    (b'', False)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context and whether it was actually stored
    :rtype: tuple[bytes, bool]
    """
    pass


def get_int(key: bytes, context: StorageContext = get_context()) -> int:
    """
    Gets a value as integer from the persistent store based on the given key.
    It's equivalent to boa3.sc.utils.to_int(get(key, context))

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


def try_get_int(key: bytes, context: StorageContext = get_context()) -> tuple[int, bool]:
    """
    Gets a value as integer from the persistent store based on the given key and returns whether the value is stored.

    >>> put_int(b'unit', 5)
    ... try_get_int(b'unit')
    (5, True)

    >>> try_get_int(b'fake_key')
    (0, False)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context and whether it was actually stored
    :rtype: tuple[int, bool]
    """
    pass


def get_bool(key: bytes, context: StorageContext = get_context()) -> bool:
    """
    Gets a value as boolean from the persistent store based on the given key.
    It's equivalent to boa3.sc.utils.to_bool(get(key, context))

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


def try_get_bool(key: bytes, context: StorageContext = get_context()) -> tuple[bool, bool]:
    """
    Gets a value as boolean from the persistent store based on the given key and returns whether the value is stored.

    >>> put_bool(b'unit', False)
    ... try_get_bool(b'unit')
    (False, True)

    >>> try_get_bool(b'fake_key')
    (False, False)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context and whether it was actually stored
    :rtype: tuple[bool, bool]
    """
    pass


def get_str(key: bytes, context: StorageContext = get_context()) -> str:
    """
    Gets a value as string from the persistent store based on the given key.
    It's equivalent to boa3.sc.utils.to_str(get(key, context))

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


def try_get_str(key: bytes, context: StorageContext = get_context()) -> tuple[str, bool]:
    """
    Gets a value as string from the persistent store based on the given key and returns whether the value is stored.

    >>> put_str(b'unit', 'test')
    ... try_get_str(b'unit')
    ('test', True)

    >>> try_get_str(b'fake_key')
    ('', False)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context and whether it was actually stored
    :rtype: tuple[str, bool]
    """
    pass


def get_list(key: bytes, context: StorageContext = get_context()) -> list:
    """
    Gets a value as list from the persistent store based on the given key.
    It's equivalent to boa3.sc.contracts.stdlib.StdLib.deserialize(get(key, context))

    >>> put_list(b'unit', [1, 2, '3'])
    ... get_list(b'unit')
    [1, 2, '3']

    >>> get_list(b'fake_key')
    []

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context
    :rtype: list
    """
    pass


def try_get_list(key: bytes, context: StorageContext = get_context()) -> tuple[list, bool]:
    """
    Gets a value as list from the persistent store based on the given key and returns whether the value is stored.

    >>> put_list(b'unit', [1, 2, '3'])
    ... try_get_list(b'unit')
    ([1, 2, '3'], True)

    >>> get_list(b'fake_key')
    ([], False)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context and whether it was actually stored
    :rtype: tuple[list, bool]
    """
    pass


def get_dict(key: bytes, context: StorageContext = get_context()) -> dict:
    """
    Gets a value as dict from the persistent store based on the given key.
    It's equivalent to boa3.sc.contracts.stdlib.StdLib.deserialize(get(key, context))

    >>> put_dict(b'unit', {'example': 1, 'other_example': 2})
    ... get_dict(b'unit')
    {'example': 1, 'other_example': 2}

    >>> get_dict(b'fake_key')
    {}

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context
    :rtype: dict
    """
    pass


def try_get_dict(key: bytes, context: StorageContext = get_context()) -> tuple[dict, bool]:
    """
    Gets a value as dict from the persistent store based on the given key and returns whether the value is stored.

    >>> put_dict(b'unit', {'example': 1, 'other_example': 2})
    ... get_dict(b'unit')
    ({'example': 1, 'other_example': 2}, True)

    >>> get_dict(b'fake_key')
    ({}, False)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context and whether it was actually stored
    :rtype: tuple[dict, bool]
    """
    pass


def get_object(key: bytes, context: StorageContext = get_context()) -> Any:
    """
    Gets a value as object from the persistent store based on the given key.
    It's equivalent to boa3.sc.contracts.stdlib.StdLib.deserialize(get(key, context))
    Returns an empty struct if not found.

    >>> example = SomeClass()
    >>> put_object(b'unit', example)
    ... get_object(b'unit')
    SomeClass

    >>> get_object(b'fake_key')
    object

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context
    :rtype: Any
    """
    pass


def try_get_object(key: bytes, context: StorageContext = get_context()) -> tuple[Any, bool]:
    """
    Gets a value as dict from the persistent store based on the given key and returns whether the value is stored.

    >>> example = SomeClass()
    >>> put_object(b'unit', example)
    ... try_get_object(b'unit')
    (SomeClass, True)

    >>> get_object(b'fake_key')
    (object, False)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context and whether it was actually stored
    :rtype: tuple[Any, bool]
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
    :rtype: boa3.sc.types.UInt160
    """
    pass


def try_get_uint160(key: bytes, context: StorageContext = get_context()) -> tuple[UInt160, bool]:
    """
    Gets a value as UInt160 from the persistent store based on the given key and returns whether the value is stored.

    >>> put_uint160(b'unit', UInt160(b'0123456789ABCDEFGHIJ'))
    ... try_get_uint160(b'unit')
    (UInt160(0x4a49484746454443424139383736353433323130), True)

    >>> get_uint160(b'fake_key')
    (UInt160(0x0000000000000000000000000000000000000000), False)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context and whether it was actually stored
    :rtype: tuple[boa3.sc.types.UInt160, bool]
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
    :rtype: boa3.sc.types.UInt256
    """
    pass


def try_get_uint256(key: bytes, context: StorageContext = get_context()) -> tuple[UInt256, bool]:
    """
    Gets a value as UInt256 from the persistent store based on the given key and returns whether the value is stored.

    >>> put_uint256(b'unit', UInt256(b'0123456789ABCDEFGHIJKLMNOPQRSTUV'))
    ... get_uint256(b'unit')
    (UInt256(0x565554535251504f4e4d4c4b4a49484746454443424139383736353433323130), True)

    >>> get_uint160(b'fake_key')
    (UInt256(0x0000000000000000000000000000000000000000000000000000000000000000), False)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context and whether it was actually stored
    :rtype: tuple[boa3.sc.types.UInt256, bool]
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
    :rtype: boa3.sc.types.ECPoint
    """
    pass


def try_get_ecpoint(key: bytes, context: StorageContext = get_context()) -> tuple[ECPoint, bool]:
    """
    Gets a value as ECPoint from the persistent store based on the given key and returns whether the value is stored.

    >>> put_ecpoint(b'unit', ECPoint(b'0123456789ABCDEFGHIJKLMNOPQRSTUVW'))
    ... try_get_ecpoint(b'unit')
    (ECPoint(0x57565554535251504f4e4d4c4b4a49484746454443424139383736353433323130), True)

    >>> try_get_ecpoint(b'fake_key')
    (ECPoint(0x000000000000000000000000000000000000000000000000000000000000000000), False)

    :param key: value identifier in the store
    :type key: bytes
    :param context: storage context to be used
    :type context: StorageContext
    :return: the value corresponding to given key for current storage context and whether it was actually stored
    :rtype: tuple[boa3.sc.types.ECPoint, bool]
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
    It's equivalent to put(key, boa3.sc.utils.to_int(value), context)

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
    It's equivalent to put(key, boa3.sc.utils.to_bool(value), context)

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
    It's equivalent to put(key, boa3.sc.utils.to_str(value), context)

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


def put_list(key: bytes, value: list, context: StorageContext = get_context()):
    """
    Inserts a given list value in the key-value format into the persistent storage.
    It's equivalent to put(key, boa3.sc.contracts.stdlib.StdLib.serialize(value), context)

    >>> put_list(b'unit', [1, 2, '3'])
    None

    :param key: the identifier in the store for the new value
    :type key: bytes
    :param value: value to be stored
    :type value: list
    :param context: storage context to be used
    :type context: StorageContext
    """
    pass


def put_dict(key: bytes, value: dict, context: StorageContext = get_context()):
    """
    Inserts a given dict value in the key-value format into the persistent storage.
    It's equivalent to put(key, boa3.sc.contracts.stdlib.StdLib.serialize(value), context)

    >>> put_dict(b'unit', {'example': 1, 'other_example': 2})
    None

    :param key: the identifier in the store for the new value
    :type key: bytes
    :param value: value to be stored
    :type value: dict
    :param context: storage context to be used
    :type context: StorageContext
    """
    pass


def put_object(key: bytes, value: object, context: StorageContext = get_context()):
    """
    Inserts a given object value in the key-value format into the persistent storage.
    It's equivalent to put(key, boa3.sc.contracts.stdlib.StdLib.serialize(value), context)

    >>> example = SomeClass()
    >>> put_object(b'unit', example)
    None

    :param key: the identifier in the store for the new value
    :type key: bytes
    :param value: value to be stored
    :type value: dict
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
    :type value: boa3.sc.types.UInt160
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
    :type value: boa3.sc.types.UInt256
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
    :type value: boa3.sc.types.ECPoint
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
    :type options: boa3.sc.types.FindOptions
    :return: an iterator with the search results
    :rtype: Iterator
    """
    pass
