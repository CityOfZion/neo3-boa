from boa3.builtin.interop.binary import base58_decode


def Main(key: int) -> str:
    return base58_decode(key)
