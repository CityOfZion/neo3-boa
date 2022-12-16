from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import ripemd160


@public
def Main() -> bytes:
    return ripemd160(10)
