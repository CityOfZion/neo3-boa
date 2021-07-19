from boa3.builtin.interop.stdlib import base58_encode


def Main(key: int) -> str:
    return base58_encode(key)
