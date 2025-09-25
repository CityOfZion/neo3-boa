__all__ = [
    'CryptoLib'
]

from boa3.sc.types import ECPoint, UInt160, NamedCurveHash, IBls12381


class CryptoLib:
    """
    A class used to represent the CryptoLib native contract.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/native/CryptoLib>`__
    to learn more about the CryptoLib class.
    """

    hash: UInt160

    @classmethod
    def recover_secp256k1(cls, message_hash: bytes, signature: bytes) -> bytes | None:
        """
        Recovers the public key from a secp256k1 signature in a single byte array format.

        >>> CryptoLib.recover_secp256k1(
        ...     bytes.fromhex('5ae8317d34d1e595e3fa7247db80c0af4320cce1116de187f8f7e2e099c0d8d0'),
        ...     bytes.fromhex('45c0b7f8c09a9e1f1cea0c25785594427b6bf8f9f878a8af0b1abbb48e16d0920d8becd0c220f67c51217eecfd7184ef0732481c843857e6bc7fc095c4f6b78801')
        ... )
        b'\x03J\x07\x1e\x8an\x10\xaa\xda+\x8c\xf3\x9f\xa3\xb5\xfb4\x00\xb0N\x99\xea\x8a\xe6L\xee\xa1\xa9w\xdb\xea\xf5\xd5'

        >>> CryptoLib.recover_secp256k1(b'unit test', b'wrong signature')
        None

        :param message_hash: the hash of the message that was signed
        :type message_hash: bytes
        :param signature: the 65-byte signature in format: r[32] + s[32] + v[1]. 64-bytes for eip-2098, where v must be 27 or 28
        :type signature: bytes
        :return: the recovered public key in compressed format, or None if recovery fails.
        :rtype: bytes
        """
        pass

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
    def sha256(cls, data: bytes) -> bytes:
        """
        Encrypts a key using SHA-256.

        >>> CryptoLib.sha256(b'unit test')
        b'\\xdau1>J\\xc2W\\xf8LN\\xfb2\\x0f\\xbd\\x01\\x1cr@<\\xf5\\x93<\\x90\\xd2\\xe3\\xb8$\\xd6H\\x96\\xf8\\x9a'

        :param data: the data to be encrypted
        :type data: bytes
        :return: a byte value that represents the encrypted key
        :rtype: bytes
        """
        pass

    @classmethod
    def ripemd160(cls, data: bytes) -> bytes:
        """
        Encrypts a key using RIPEMD-160.

        >>> CryptoLib.ripemd160(b'unit test')
        b'H\\x8e\\xef\\xf4Zh\\x89:\\xe6\\xf1\\xdc\\x08\\xdd\\x8f\\x01\\rD\\n\\xbdH'

        :param data: the data to be encrypted
        :type data: Any
        :return: a byte value that represents the encrypted key
        :rtype: bytes
        """
        pass

    @classmethod
    def keccak256(cls, data: bytes) -> bytes:
        """
        Computes the hash value for the specified byte array using the keccak256 algorithm.

        >>> CryptoLib.keccak256(b'unit test')
        b'\\xe5\\x26\\x91\\x5a\\xff\\x6f\\x5e\\x35\\x9d\\x64\\xa3\\xce\\xf0\\x6e\\xf3\\xdb\\x9f\\x4a\\x89\\x0e\\x20\\xd1\\xa5\\x19\\x5e\\x3a\\x24\\x29\\x78\\x7e\\xec\\xb7'

        :param data: the input to compute the hash code for
        :type data: bytes
        :return: computed hash
        :rtype: bytes
        """
        pass

    @classmethod
    def verify_with_ecdsa(cls, message: bytes, pubkey: ECPoint, signature: bytes, curve: NamedCurveHash) -> bool:
        """
        Using the elliptic curve, it checks if the signature of the message was originally produced by the public key.

        >>> CryptoLib.verify_with_ecdsa(b'unit test', ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a'),
        ...                             b'wrong_signature', NamedCurveHash.SECP256R1SHA256)
        False

        :param message: the encrypted message
        :type message: bytes
        :param pubkey: the public key that might have created the item
        :type pubkey: boa3.sc.types.ECPoint
        :param signature: the signature of the item
        :type signature: bytes
        :param curve: the curve that will be used by the ecdsa
        :type curve: boa3.sc.type.NamedCurveHash
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
