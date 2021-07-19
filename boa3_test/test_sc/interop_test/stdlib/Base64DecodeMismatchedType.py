from boa3.builtin.interop.stdlib import base64_decode


def Main(key: int) -> str:
    return base64_decode(key)
