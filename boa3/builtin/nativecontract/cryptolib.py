from typing import Any

from boa3.builtin.type import ECPoint


class CryptoLib:
    """
    A class used to represent the CryptoLib native contract
    """

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

    # TODO: Change it to verify_with_ecdsa when implemented
    @classmethod
    def verify_with_ecdsa_secp256k1(cls, item: Any, pubkey: ECPoint, signature: bytes) -> bool:
        """
        Using the elliptic curve secp256k1, it checks if the signature of the any item was originally produced by the
        public key.

        :param item: the encrypted message
        :type item: Any
        :param pubkey: the public key that might have created the item
        :type pubkey: ECPoint
        :param signature: the signature of the item
        :type signature: bytes
        :return: a boolean value that represents whether the signature is valid
        :rtype: bool
        """
        pass

    # TODO: Change it to verify_with_ecdsa when implemented
    @classmethod
    def verify_with_ecdsa_secp256r1(cls, item: Any, pubkey: ECPoint, signature: bytes) -> bool:
        """
        Using the elliptic curve secp256r1, it checks if the signature of the any item was originally produced by the
        public key.

        :param item: the encrypted message
        :type item: Any
        :param pubkey: the public key that might have created the item
        :type pubkey: ECPoint
        :param signature: the signature of the item
        :type signature: bytes
        :return: a boolean value that represents whether the signature is valid
        :rtype: bool
        """
        pass
