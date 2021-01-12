from boa3.builtin import public
from boa3.builtin.interop.binary import base64_encode


@public
def Main(key: bytes) -> str:
    return base64_encode(key)
