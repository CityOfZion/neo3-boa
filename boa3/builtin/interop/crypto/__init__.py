from typing import Any, List


def sha256(key: Any) -> bytes:
    pass


def ripemd160(key: Any) -> bytes:
    pass


def hash160(key: Any) -> bytes:
    pass


def hash256(key: Any) -> bytes:
    pass


def check_multisig_with_ecdsa_secp256r1(item: Any, pubkeys: List[bytes], signatures: List[bytes]) -> bool:
    pass


def check_multisig_with_ecdsa_secp256k1(item: Any, pubkeys: List[bytes], signatures: List[bytes]) -> bool:
    pass


def verify_with_ecdsa_secp256r1(item: Any, pubkey: bytes, signature: bytes) -> bool:
    """
    Using the elliptic curve secp256r1, it checks if the signature of the any item was originally produced by the public key.

    :param item: the encrypted message
    :type item: Any
    :param pubkey: the public key that might have created the item
    :type pubkey: bytes
    :param signature: the signature of the item
    :type signature: bytes
    :return:: a boolean value that represents whether the signature is valid
    :rtype: bool
    """
    pass


def verify_with_ecdsa_secp256k1(item: Any, pubkey: bytes, signature: bytes) -> bool:
    """
    Using the elliptic curve secp256k1, it checks if the signature of the any item was originally produced by the public key.

    :param item: the encrypted message
    :type item: Any
    :param pubkey: the public key that might have created the item
    :type pubkey: bytes
    :param signature: the signature of the item
    :type signature: bytes
    :return:: a boolean value that represents whether the signature is valid
    :rtype: bool
    """
    pass
