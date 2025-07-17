from enum import IntEnum


class NamedCurveHash(IntEnum):
    """
    Represents the named curve used in ECDSA.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/foundation/Cryptography/encryption_algorithm#ecdsa-signing>`__
    to learn more about ECDSA signing.
    """

    SECP256K1SHA256 = 22
    """
    The secp256k1 curve and SHA256 hash algorithm.

    :meta hide-value: 
    """

    SECP256R1SHA256 = 23
    """
    The secp256r1 curve, which known as prime256v1 or nistP-256, and SHA256 hash algorithm.

    :meta hide-value:
    """

    SECP256K1KECCAK256 = 122
    """
    The secp256k1 curve and Keccak256 hash algorithm.

    :meta hide-value:
    """

    SECP256R1KECCAK256 = 123
    """
    The secp256r1 curve, which known as prime256v1 or nistP-256, and Keccak256 hash algorithm.

    :meta hide-value:
    """
