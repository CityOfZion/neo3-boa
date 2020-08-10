from boa3.builtin.interop.binary import base58_encode


def Main(key: int) -> bytes:
    return base58_encode(key)
