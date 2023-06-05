__all__ = [
    'CryptoLib',
    'NamedCurve',
]

from typing import Any

from boa3.builtin.interop.crypto import NamedCurve
from boa3.builtin.type import ECPoint, UInt160


class CryptoLib:
    """
    A class used to represent the CryptoLib native contract
    """

    hash: UInt160

    @classmethod
    def murmur32(cls, data: bytes, seed: int) -> bytes:
        """
        Computes the hash value for the specified byte array using the murmur32 algorithm.

        :param data: the input to compute the hash code for
        :type data: bytes
        :param seed: the seed of the murmur32 hash function
        :type seed: int
        :return: the hash value
        :rtype: bytes
        """
        pass

    @classmethod
    def sha256(cls, key: Any) -> bytes:
        """
        Encrypts a key using SHA-256.

        :param key: the key to be encrypted
        :type key: Any
        :return: a byte value that represents the encrypted key
        :rtype: bytes
        """
        pass

    @classmethod
    def ripemd160(cls, key: Any) -> bytes:
        """
        Encrypts a key using RIPEMD-160.

        :param key: the key to be encrypted
        :type key: Any
        :return: a byte value that represents the encrypted key
        :rtype: bytes
        """
        pass

    @classmethod
    def verify_with_ecdsa(cls, message: bytes, pubkey: ECPoint, signature: bytes, curve: NamedCurve) -> bool:
        """
        Using the elliptic curve, it checks if the signature of the message was originally produced by the public key.

        :param message: the encrypted message
        :type message: bytes
        :param pubkey: the public key that might have created the item
        :type pubkey: ECPoint
        :param signature: the signature of the item
        :type signature: bytes
        :param curve: the curve that will be used by the ecdsa
        :type curve: NamedCurve
        :return: a boolean value that represents whether the signature is valid
        :rtype: bool
        """
        pass
