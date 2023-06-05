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
    """
    pass


def to_str(value: bytes) -> str:
    """
    Converts a bytes value to a string.
    """
    pass


def to_int(value: bytes) -> int:
    """
    Converts a bytes value to the integer it represents.
    """
    pass


def to_bool(value: bytes) -> bool:
    """
    Return a bytes value to the boolean it represents.
    """
    pass
