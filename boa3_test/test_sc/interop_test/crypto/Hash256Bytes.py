from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import hash256


@public
def Main() -> bytes:
    return hash256(b'unit test')
