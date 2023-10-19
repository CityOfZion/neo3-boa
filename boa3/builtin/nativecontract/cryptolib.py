__all__ = [
    'CryptoLib',
    'NamedCurve',
    'IBls12381'
]

from typing import Any

from boa3.builtin.interop.crypto import NamedCurve, IBls12381
from boa3.builtin.type import ECPoint, UInt160


class CryptoLib:
    """
    A class used to represent the CryptoLib native contract.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/native/CryptoLib>`__
    to learn more about the CryptoLib class.
    """

    hash: UInt160

    @classmethod
    def murmur32(cls, data: bytes, seed: int) -> bytes:
        """
        Computes the hash value for the specified byte array using the murmur32 algorithm.

        >>> CryptoLib.murmur32(b'unit test', 0)
        b"\\x90D'G"

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

        >>> CryptoLib.sha256('unit test')
        b'\\xdau1>J\\xc2W\\xf8LN\\xfb2\\x0f\\xbd\\x01\\x1cr@<\\xf5\\x93<\\x90\\xd2\\xe3\\xb8$\\xd6H\\x96\\xf8\\x9a'

        >>> CryptoLib.sha256(10)
        b'\\x9c\\x82r\\x01\\xb9@\\x19\\xb4/\\x85pk\\xc4\\x9cY\\xff\\x84\\xb5`M\\x11\\xca\\xaf\\xb9\\n\\xb9HV\\xc4\\xe1\\xddz'

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

        >>> CryptoLib.ripemd160('unit test')
        b'H\\x8e\\xef\\xf4Zh\\x89:\\xe6\\xf1\\xdc\\x08\\xdd\\x8f\\x01\\rD\\n\\xbdH'

        >>> CryptoLib.ripemd160(10)
        b'\\xc0\\xda\\x02P8\\xed\\x83\\xc6\\x87\\xdd\\xc40\\xda\\x98F\\xec\\xb9\\x7f9\\x98'

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

        >>> CryptoLib.verify_with_ecdsa(b'unit test', ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a'),
        ...                             b'wrong_signature', NamedCurve.SECP256R1)
        False

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

    @classmethod
    def bls12_381_add(cls, x: IBls12381, y: IBls12381) -> IBls12381:
        """
        Add operation of two bls12381 points.

        :param x: The first point
        :type x: IBls12381
        :param y: The second point
        :type y: IBls12381
        :return: the two points sum
        :rtype: IBls12381
        """
        pass

    @classmethod
    def bls12_381_deserialize(cls, data: bytes) -> IBls12381:
        """
        Deserialize a bls12381 point.

        :param data: The point as byte array
        :type data: bytes
        :return: the deserialized point
        :rtype: IBls12381
        """
        pass

    @classmethod
    def bls12_381_equal(cls, x: IBls12381, y: IBls12381) -> bool:
        """
        Determines whether the specified points are equal.

        :param x: The first point
        :type x: IBls12381
        :param y: The second point
        :type y: IBls12381
        :return: whether the specified points are equal or not
        :rtype: bool
        """
        pass

    @classmethod
    def bls12_381_mul(cls, x: IBls12381, mul: bytes, neg: bool) -> IBls12381:
        """
        Mul operation of gt point and multiplier.

        :param x: The point
        :type x: IBls12381
        :param mul: Multiplier, 32 bytes, little-endian
        :type mul: int
        :param neg: negative number
        :type neg: bool
        :return: the two points product
        :rtype: IBls12381
        """
        pass

    @classmethod
    def bls12_381_pairing(cls, g1: IBls12381, g2: IBls12381) -> IBls12381:
        """
        Pairing operation of g1 and g2.

        :param g1: The g1 point
        :type g1: IBls12381
        :param g2: The g2 point
        :type g2: IBls12381
        :return: the two points pairing
        :rtype: IBls12381
        """
        pass

    @classmethod
    def bls12_381_serialize(cls, g: IBls12381) -> bytes:
        """
        Serialize a bls12381 point.

        :param g: The point to be serialized.
        :type g: IBls12381
        :return: the serialized point
        :rtype: bytes
        """
        pass
