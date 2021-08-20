from enum import IntFlag


class NamedCurve(IntFlag):
    """
    Represents the named curve used in ECDSA.
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
