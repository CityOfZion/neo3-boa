from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import sha256


@public
def Main(test: str) -> bytes:
    return sha256(test)
