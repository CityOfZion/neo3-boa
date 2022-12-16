from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import hash160


@public
def Main() -> bytes:
    return hash160(b'unit test')
