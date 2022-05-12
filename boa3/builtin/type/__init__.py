from __future__ import annotations

from typing import Sequence, Union


class UInt160(bytes):
    """
    Represents a 160-bit unsigned integer.
    """

    def __init__(self, arg: Union[bytes, int] = 0):
        super().__init__()
        pass


class UInt256(bytes):
    """
    Represents a 256-bit unsigned integer.
    """

    def __init__(self, arg: Union[bytes, int] = 0):
        super().__init__()
        pass


class ECPoint(bytes):
    """
    Represents a coordinate pair for elliptic curve cryptography (ECC) structures.
    """

    def __init__(self, arg: bytes):
        super().__init__()
        pass

    def to_script_hash(self) -> bytes:
        """
        Converts a data to a script hash.

        :return: the script hash of the data
        :rtype: bytes
        """
        pass


class ByteString:
    """
    An type annotation for values that can be str or bytes. Same as Union[str, bytes]
    """

    def to_bytes(self) -> bytes:
        """
        Converts an ByteString value to an array of bytes
        """
        pass

    def to_str(self) -> str:
        """
        Converts an ByteString value to a string.
        """
        pass

    def to_int(self) -> int:
        """
        Return the integer represented by this ByteString.
        """
        pass

    def to_bool(self) -> bool:
        """
        Return the boolean represented by this ByteString.
        """
        pass

    def isdigit(self) -> bool:
        """
        Return True if the ByteString is a digit string, False otherwise.

        A ByteString is a digit string if all characters in the ByteString are digits and there
        is at least one character in the ByteString.
        """
        pass

    def join(self, __iterable: Sequence[ByteString]) -> ByteString:
        """
        S.join(__iterable: Sequence[ByteString]) -> ByteString

        Concatenate any number of ByteStrings.

        The ByteString whose method is called is inserted in between each given ByteString.
        The result is returned as a new ByteString.
        """
        pass

    def lower(self) -> ByteString:
        """
        S.lower() -> ByteString

        Return a copy of the ByteString converted to lowercase.
        """
        pass

    def startswith(self, prefix: ByteString, start: int = 0, end: int = -1) -> bool:
        """
        S.startswith(prefix: ByteString, start: int, end: int) -> bool

        Return True if S starts with the specified prefix, False otherwise.
        With optional start, test S beginning at that position.
        With optional end, stop comparing S at that position.
        prefix can also be a tuple of strings to try.
        """
        pass

    def strip(self, __chars: ByteString) -> ByteString:
        """
        S.strip(__chars: ByteString) -> ByteString

        Return a copy of the ByteString with leading and trailing whitespace remove.

        If chars is given and not None, remove characters in chars instead.
        """
        pass

    def upper(self) -> ByteString:
        """
        S.upper() -> ByteString

        Return a copy of the ByteString converted to uppercase.
        """
        pass

    def __add__(self, *args, **kwargs):  # real signature unknown
        """
        Return self+value.
        """
        pass

    def __mul__(self, *args, **kwargs):  # real signature unknown
        """
        Return self*value.
        """
        pass

    def __rmul__(self, *args, **kwargs):  # real signature unknown
        """
        Return value*self.
        """
        pass
