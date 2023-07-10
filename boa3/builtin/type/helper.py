__all__ = [
    'to_bool',
    'to_bytes',
    'to_int',
    'to_str',
]

from typing import Union


def to_bytes(value: Union[str, int]) -> bytes:
    """
    Converts a str or integer value to an array of bytes

    >>> to_bytes(65)
    b'A'

    >>> to_bytes('A')
    b'A'
    """
    pass


def to_str(value: bytes) -> str:
    """
    Converts a bytes value to a string.

    >>> to_str(b'A')
    'A'
    """
    pass


def to_int(value: bytes) -> int:
    """
    Converts a bytes value to the integer it represents.

    >>> to_int(b'A')
    65
    """
    pass


def to_bool(value: bytes) -> bool:
    """
    Return a bytes value to the boolean it represents.

    >>> to_bool(b'\\x00')
    False

    >>> to_bool(b'\\x01')
    True

    >>> to_bool(b'\\x02')
    True
    """
    pass
