from boa3.builtin.interop.stdlib import base58_decode


def Main(key: int) -> bytes:
    return base58_decode(key)
