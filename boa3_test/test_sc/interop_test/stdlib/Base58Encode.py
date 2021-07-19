from boa3.builtin import public
from boa3.builtin.interop.stdlib import base58_encode


@public
def Main(key: bytes) -> str:
    return base58_encode(key)
