from __future__ import annotations

__all__ = [
    'Event',
    'UInt160',
    'UInt256',
    'ECPoint',
    'Address',
    'BlockHash',
    'PublicKey',
    'ScriptHash',
    'ScriptHashLittleEndian',
    'TransactionId',
]

from typing import Union


class Event:
    """
    Describes an action that happened in the blockchain.
    """
    pass


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


class Address(str):
    """
    A class used only to indicate that a parameter or return on the manifest should be treated as an Address.
    It's a subclass of str and it doesn't implement new properties or methods.
    """
    pass


class BlockHash(UInt256):
    """
    A class used only to indicate that a parameter or return on the manifest should be treated as a BlockHash.
    It's a subclass of UInt256 and it doesn't implement new properties or methods.
    """
    pass


class PublicKey(ECPoint):
    """
    A class used only to indicate that a parameter or return on the manifest should be treated as a PublicKey.
    It's a subclass of ECPoint and it doesn't implement new properties or methods.
    """
    pass


class ScriptHash(UInt160):
    """
    A class used only to indicate that a parameter or return on the manifest should be treated as a ScriptHash.
    It's a subclass of UInt160 and it doesn't implement new properties or methods.
    """
    pass


class ScriptHashLittleEndian(UInt160):
    """
    A class used only to indicate that a parameter or return on the manifest should be treated as a
    ScriptHashLittleEndian.
    It's a subclass of UInt160 and it doesn't implement new properties or methods.
    """
    pass


class TransactionId(UInt256):
    """
    A class used only to indicate that a parameter or return on the manifest should be treated as a TransactionId.
    It's a subclass of UInt256 and it doesn't implement new properties or methods.
    """
    pass
