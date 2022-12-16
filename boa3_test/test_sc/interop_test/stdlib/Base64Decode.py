from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import base64_decode


@public
def Main(key: str) -> bytes:
    return base64_decode(key)
