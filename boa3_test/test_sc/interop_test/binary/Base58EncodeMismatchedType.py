from boa3.builtin.interop.binary import base58_encode


def Main(key: int) -> str:
    return base58_encode(key)
