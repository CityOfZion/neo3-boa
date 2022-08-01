from typing import Any

from boa3.builtin.interop.crypto import NamedCurve
from boa3.builtin.type import ByteString, ECPoint


class CryptoLib:
    """
    A class used to represent the CryptoLib native contract
    """

    @classmethod
    def murmur32(cls, data: ByteString, seed: int) -> ByteString:
        """
        Computes the hash value for the specified byte array using the murmur32 algorithm.

        :param data: the input to compute the hash code for
        :type data: ByteString
        :param seed: the seed of the murmur32 hash function
        :type seed: int
        :return: the hash value
        :rtype: ByteString
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
    def verify_with_ecdsa(cls, message: Any, pubkey: ECPoint, signature: ByteString, curve: NamedCurve) -> bool:
        """
        Using the elliptic curve, it checks if the signature of the any item was originally produced by the public key.

        :param message: the encrypted message
        :type message: Any
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
