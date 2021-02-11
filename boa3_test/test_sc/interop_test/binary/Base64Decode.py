from boa3.builtin import public
from boa3.builtin.interop.binary import base64_decode


@public
def Main(key: str) -> bytes:
    return base64_decode(key)
