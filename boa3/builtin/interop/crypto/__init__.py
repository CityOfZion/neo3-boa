__all__ = [
    'NamedCurve',
    'IBls12381',
    'sha256',
    'ripemd160',
    'hash160',
    'hash256',
    'check_sig',
    'check_multisig',
    'verify_with_ecdsa',
    'murmur32',
    'bls12_381_add',
    'bls12_381_deserialize',
    'bls12_381_equal',
    'bls12_381_mul',
    'bls12_381_pairing',
    'bls12_381_serialize',
]


from typing import Any, List

from boa3.builtin.interop.crypto.ibls12381 import IBls12381
from boa3.builtin.interop.crypto.namedcurve import NamedCurve
from boa3.builtin.type import ECPoint


def sha256(key: Any) -> bytes:
    """
    Encrypts a key using SHA-256.

    >>> sha256('unit test')
    b'\\xdau1>J\\xc2W\\xf8LN\\xfb2\\x0f\\xbd\\x01\\x1cr@<\\xf5\\x93<\\x90\\xd2\\xe3\\xb8$\\xd6H\\x96\\xf8\\x9a'

    >>> sha256(10)
    b'\\x9c\\x82r\\x01\\xb9@\\x19\\xb4/\\x85pk\\xc4\\x9cY\\xff\\x84\\xb5`M\\x11\\xca\\xaf\\xb9\\n\\xb9HV\\xc4\\xe1\\xddz'

    :param key: the key to be encrypted
    :type key: Any
    :return: a byte value that represents the encrypted key
    :rtype: bytes
    """
    pass


def ripemd160(key: Any) -> bytes:
    """
    Encrypts a key using RIPEMD-160.

    >>> ripemd160('unit test')
    b'H\\x8e\\xef\\xf4Zh\\x89:\\xe6\\xf1\\xdc\\x08\\xdd\\x8f\\x01\\rD\\n\\xbdH'

    >>> ripemd160(10)
    b'\\xc0\\xda\\x02P8\\xed\\x83\\xc6\\x87\\xdd\\xc40\\xda\\x98F\\xec\\xb9\\x7f9\\x98'

    :param key: the key to be encrypted
    :type key: Any
    :return: a byte value that represents the encrypted key
    :rtype: bytes
    """
    pass


def hash160(key: Any) -> bytes:
    """
    Encrypts a key using HASH160.

    >>> hash160('unit test')
    b'#Q\\xc9\\xaf+c\\x12\\xb1\\xb9\\x9e\\xa1\\x89t\\xa228g\\xec\\x0eF'

    >>> hash160(10)
    b'\\x89\\x86D\\x19\\xa8\\xc3v%\\x00\\xfe\\x9a\\x98\\xaf\\x8f\\xbbO3u\\x08\\xf0'

    :param key: the key to be encrypted
    :type key: Any
    :return: a byte value that represents the encrypted key
    :rtype: bytes
    """
    pass


def hash256(key: Any) -> bytes:
    """
    Encrypts a key using HASH256.

    >>> hash256('unit test')
    b'\\xdau1>J\\xc2W\\xf8LN\\xfb2\\x0f\\xbd\\x01\\x1cr@<\\xf5\\x93<\\x90\\xd2\\xe3\\xb8$\\xd6H\\x96\\xf8\\x9a'

    >>> hash256(10)
    b'\\x9c\\x82r\\x01\\xb9@\\x19\\xb4/\\x85pk\\xc4\\x9cY\\xff\\x84\\xb5`M\\x11\\xca\\xaf\\xb9\\n\\xb9HV\\xc4\\xe1\\xddz'

    :param key: the key to be encrypted
    :type key: Any
    :return: a byte value that represents the encrypted key
    :rtype: bytes
    """
    pass


def check_sig(pub_key: ECPoint, signature: bytes) -> bool:
    """
    Checks the signature for the current script container.

    >>> check_sig(ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a'),
    ...           b'wrongsignature')
    False

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

    >>> check_multisig([ECPoint(b"\\x03\\xcd\\xb0\\x67\\xd9\\x30\\xfd\\x5a\\xda\\xa6\\xc6\\x85\\x45\\x01\\x60\\x44\\xaa\\xdd\\xec\\x64\\xba\\x39\\xe5\\x48\\x25\\x0e\\xae\\xa5\\x51\\x17\\x2e\\x53\\x5c"),
    ...                 ECPoint(b"\\x03l\\x841\\xccx\\xb31w\\xa6\\x0bK\\xcc\\x02\\xba\\xf6\\r\\x05\\xfe\\xe5\\x03\\x8es9\\xd3\\xa6\\x88\\xe3\\x94\\xc2\\xcb\\xd8C")],
    ...                [b'wrongsignature1', b'wrongsignature2'])
    False

    :param pubkeys: a list of public keys
    :type pubkeys: List[ECPoint]
    :param signatures: a list of signatures
    :type signatures: List[bytes]
    :return: a boolean value that represents whether the signatures were validated
    :rtype: bool
    """
    pass


def verify_with_ecdsa(message: bytes, pubkey: ECPoint, signature: bytes, curve: NamedCurve) -> bool:
    """
    Using the elliptic curve, it checks if the signature of the message was originally produced by the public key.

    >>> verify_with_ecdsa(b'unit test', ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a'),
    ...                   b'wrong_signature', NamedCurve.SECP256R1)
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


def murmur32(data: bytes, seed: int) -> bytes:
    """
    Computes the hash value for the specified byte array using the murmur32 algorithm.

    >>> murmur32(b'unit test', 0)
    b"\\x90D'G"

    :param data: the input to compute the hash code for
    :type data: bytes
    :param seed: the seed of the murmur32 hash function
    :type seed: int
    :return: the hash value
    :rtype: bytes
    """
    pass


def bls12_381_add(x: IBls12381, y: IBls12381) -> IBls12381:
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


def bls12_381_deserialize(data: bytes) -> IBls12381:
    """
    Deserialize a bls12381 point.

    :param data: The point as byte array
    :type data: bytes
    :return: the deserialized point
    :rtype: IBls12381
    """
    pass


def bls12_381_equal(x: IBls12381, y: IBls12381) -> bool:
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


def bls12_381_mul(x: IBls12381, mul: bytes, neg: bool) -> IBls12381:
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


def bls12_381_pairing(g1: IBls12381, g2: IBls12381) -> IBls12381:
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


def bls12_381_serialize(g: IBls12381) -> bytes:
    """
    Serialize a bls12381 point.

    :param g: The point to be serialized.
    :type g: IBls12381
    :return: the serialized point
    :rtype: bytes
    """
    pass
