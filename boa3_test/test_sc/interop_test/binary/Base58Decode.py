from boa3.builtin import public
from boa3.builtin.interop.binary import base58_decode


@public
def Main(key: str) -> bytes:
    return base58_decode(key)
