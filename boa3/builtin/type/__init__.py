from typing import Union


class UInt160(bytes):
    """
    Represents a 160-bit unsigned integer.
    """

    def __init__(self, arg: Union[bytes, int] = 0):
        super().__init__()
        pass


class UInt256(bytes):
    """
    Represents a 256-bit unsigned integer.
    """

    def __init__(self, arg: Union[bytes, int] = 0):
        super().__init__()
        pass


class ECPoint(bytes):
    """
    Represents a coordinate pair for elliptic curve cryptography (ECC) structures.
    """

    def __init__(self, arg: bytes):
        super().__init__()
        pass
