from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import base64_encode


@public
def Main(key: bytes) -> str:
    return base64_encode(key)
