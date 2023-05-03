from typing import Any, List

from boa3.builtin.interop.crypto.namedcurve import NamedCurve
from boa3.builtin.type import ByteString, ECPoint


def sha256(key: Any) -> bytes:
    """
    Encrypts a key using SHA-256.

    :param key: the key to be encrypted
    :type key: Any
    :return: a byte value that represents the encrypted key
    :rtype: bytes
    """
    pass


def ripemd160(key: Any) -> bytes:
    """
    Encrypts a key using RIPEMD-160.

    :param key: the key to be encrypted
    :type key: Any
    :return: a byte value that represents the encrypted key
    :rtype: bytes
    """
    pass


def hash160(key: Any) -> bytes:
    """
    Encrypts a key using HASH160.

    :param key: the key to be encrypted
    :type key: Any
    :return: a byte value that represents the encrypted key
    :rtype: bytes
    """
    pass


def hash256(key: Any) -> bytes:
    """
    Encrypts a key using HASH256.

    :param key: the key to be encrypted
    :type key: Any
    :return: a byte value that represents the encrypted key
    :rtype: bytes
    """
    pass


def check_sig(pub_key: ECPoint, signature: bytes) -> bool:
    """
    Checks the signature for the current script container.

    :param pub_key: the public key of the account
    :type pub_key: ECPoint
    :param signature: the signature of the current script container
    :type signature: bytes
    :return: whether the signature is valid or not
    :rtype: bool
    """
    pass


def check_multisig(pubkeys: List[ECPoint], signatures: List[bytes]) -> bool:
    """
    Checks the signatures for the current script container.

    :param pubkeys: a list of public keys
    :type pubkeys: List[ECPoint]
    :param signatures: a list of signatures
    :type signatures: List[bytes]
    :return: a boolean value that represents whether the signatures were validated
    :rtype: bool
    """
    pass


def verify_with_ecdsa(message: ByteString, pubkey: ECPoint, signature: ByteString, curve: NamedCurve) -> bool:
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


def murmur32(data: ByteString, seed: int) -> ByteString:
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


def bls12_381_add(x: bytes, y: bytes) -> bytes:
    """
    Add operation of two bls12381 points.

    :param x: The first point
    :type x: bytes
    :param y: The second point
    :type y: bytes
    :return: the two points sum
    :rtype: bytes
    """
    pass


def bls12_381_deserialize(data: bytes) -> bytes:
    """
    Deserialize a bls12381 point.

    :param data: The point as byte array
    :type data: bytes
    :return: the deserialized point
    :rtype: bytes
    """
    pass


def bls12_381_equal(x: bytes, y: bytes) -> bool:
    """
    Determines whether the specified points are equal.

    :param x: The first point
    :type x: bytes
    :param y: The second point
    :type y: bytes
    :return: whether the specified points are equal or not
    :rtype: bool
    """
    pass


def bls12_381_mul(x: bytes, mul: int, neg: bool) -> bytes:
    """
    Mul operation of gt point and multiplier.

    :param x: The point
    :type x: bytes
    :param mul: Multiplier, 32 bytes, little-endian
    :type mul: int
    :param neg: negative number
    :type neg: bool
    :return: the two points product
    :rtype: bytes
    """
    pass


def bls12_381_pairing(g1: bytes, g2: bytes) -> bytes:
    """
    Pairing operation of g1 and g2.

    :param g1: The g1 point
    :type g1: bytes
    :param g2: The g2 point
    :type g2: bytes
    :return: the two points pairing
    :rtype: bytes
    """
    pass


def bls12_381_serialize(g: bytes) -> bytes:
    """
    Serialize a bls12381 point.

    :param g: The point to be serialized.
    :type g: bytes
    :return: the serialized point
    :rtype: bytes
    """
    pass
