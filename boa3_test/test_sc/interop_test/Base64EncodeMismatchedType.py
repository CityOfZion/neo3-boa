from boa3.builtin.interop.binary import base64_encode


def Main(key: int) -> bytes:
    return base64_encode(key)
