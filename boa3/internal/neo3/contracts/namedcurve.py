from enum import IntFlag


class NamedCurve(IntFlag):
    """
    Represents the named curve used in ECDSA.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/foundation/Cryptography/encryption_algorithm#ecdsa-signing>`__
    to learn more about ECDSA signing.
    """

    SECP256K1 = 22
    """
    The secp256k1 curve.

    :meta hide-value: 
    """

    SECP256R1 = 23
    """
    The secp256r1 curve, which known as prime256v1 or nistP-256.

    :meta hide-value:
    """
