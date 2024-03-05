__all__ = [
    'base58_encode',
    'base58_decode',
    'base58_check_encode',
    'base58_check_decode',
    'base64_encode',
    'base64_decode',
    'serialize',
    'deserialize',
    'atoi',
    'itoa',
    'memory_search',
    'memory_compare',
]


from typing import Any


def base58_encode(key: bytes) -> str:
    """
    Encodes a bytes value using base58.

    >>> base58_encode(b'unit test')
    b"2VhL46g69A1mu"

    :param key: bytes value to be encoded
    :type key: bytes
    :return: the encoded string
    :rtype: str
    """
    pass


def base58_decode(key: str) -> bytes:
    """
    Decodes a string value encoded with base58.

    >>> base58_decode('2VhL46g69A1mu')
    b"unit test"

    :param key: string value to be decoded
    :type key: str
    :return: the decoded bytes
    :rtype: bytes
    """
    pass


def base58_check_encode(key: bytes) -> str:
    """
    Converts a bytes value to its equivalent str representation that is encoded with base-58 digits. The encoded str
    contains the checksum of the binary data.

    >>> base58_check_encode(b'unit test')
    b"AnJcKqvgBwKxsjX75o"

    :param key: bytes value to be encoded
    :type key: bytes
    :return: the encoded string
    :rtype: str
    """
    pass


def base58_check_decode(key: str) -> bytes:
    """
    Converts the specified str, which encodes binary data as base-58 digits, to an equivalent bytes value. The encoded
    str contains the checksum of the binary data.

    >>> base58_check_decode('AnJcKqvgBwKxsjX75o')
    b"unit test"

    :param key: string value to be decoded
    :type key: str
    :return: the decoded bytes
    :rtype: bytes
    """
    pass


def base64_encode(key: bytes) -> str:
    """
    Encodes a bytes value using base64.

    >>> base64_encode(b'unit test')
    b"dW5pdCB0ZXN0"

    :param key: bytes value to be encoded
    :type key: bytes
    :return: the encoded string
    :rtype: str
    """
    pass


def base64_decode(key: str) -> bytes:
    """
    Decodes a string value encoded with base64.

    >>> base64_decode("dW5pdCB0ZXN0")
    b"unit test"

    :param key: string value to be decoded
    :type key: str
    :return: the decoded bytes
    :rtype: bytes
    """
    pass


def serialize(item: Any) -> bytes:
    """
    Serializes the given value into its bytes representation.

    >>> serialize('42')
    b'(\x0242'

    >>> serialize(42)
    b'!\x01*'

    >>> serialize([2, 3, 5, 7])
    b'@\x04!\x01\x02!\x01\x03!\x01\x05!\x01\x07'

    >>> serialize({1: 1, 2: 1, 3: 2})
    b'H\x03!\x01\x01!\x01\x01!\x01\x02!\x01\x01!\x01\x03!\x01\x02'

    :param item: value to be serialized
    :type item: Any
    :return: the serialized value
    :rtype: bytes

    :raise Exception: raised if the item's type is not serializable.
    """
    pass


def deserialize(data: bytes) -> Any:
    """
    Deserializes the given bytes value.

    >>> deserialize(b'(\x0242')
    '42'

    >>> deserialize(b'!\x01*')
    42

    >>> deserialize(b'@\x04!\x01\x02!\x01\x03!\x01\x05!\x01\x07')
    [2, 3, 5, 7]

    >>> deserialize(b'H\x03!\x01\x01!\x01\x01!\x01\x02!\x01\x01!\x01\x03!\x01\x02')
    {1: 1, 2: 1, 3: 2}

    :param data: serialized value
    :type data: bytes
    :return: the deserialized result
    :rtype: Any

    :raise Exception: raised when the date doesn't represent a serialized value.
    """
    pass


def atoi(value: str, base: int = 10) -> int:
    """
    Converts a character string to a specific base value, decimal or hexadecimal. The default is decimal.

    >>> atoi('10')
    10

    >>> atoi('123')
    123

    >>> atoi('1f', 16)
    31

    >>> atoi('ff', 16)
    -1

    :param value: the int value as a string
    :type value: str
    :param base: the value base
    :type base: int
    :return: the equivalent value
    :rtype: int

    :raise Exception: raised when base isn't 10 or 16.
    """
    pass


def itoa(value: int, base: int = 10) -> str:
    """
    Converts the specific type of value to a decimal or hexadecimal string. The default is decimal.

    >>> itoa(10)
    '10'

    >>> itoa(123)
    '123'

    >>> itoa(-1, 16)
    'f'

    >>> itoa(15, 16)
    '0f'

    :param value: the int value
    :type value: int
    :param base: the value's base
    :type base: int
    :return: the converted string
    :rtype: int
    """
    pass


def memory_search(mem: bytes | str, value: bytes | str, start: int = 0, backward: bool = False) -> int:
    """
    Searches for a given value in a given memory.

    >>> memory_search('abcde', 'a', 0)
    0

    >>> memory_search('abcde', 'e', 0)
    4

    :param mem: the memory
    :type mem: bytes or str
    :param value: the value
    :type value: bytes or str
    :param start: the index the search should start from
    :type start: int
    :param backward: whether it should invert the memory
    :type backward: bool

    :return: the index of the value in the memory. Returns -1 if it's not found
    :rtype: int
    """
    pass


def memory_compare(mem1: bytes | str, mem2: bytes | str) -> int:
    """
    Compares a memory with another one.

    >>> memory_compare('abc', 'abc')
    0

    >>> memory_compare('ABC', 'abc')
    -1

    >>> memory_compare('abc', 'ABC')
    1

    :param mem1: a memory to be compared to another one
    :type mem1: bytes or str
    :param mem2: a memory that will be compared with another one
    :type mem2: bytes or str

    :return: -1 if mem1 precedes mem2, 0 if mem1 and mem2 are equal, 1 if mem1 follows mem2
    :rtype: int
    """
    pass
