from boa3.builtin import public
from boa3.builtin.interop.crypto import ripemd160


@public
def Main(test: str) -> bytes:
    return ripemd160(test)
