from boa3.builtin import public
from boa3.builtin.interop.crypto import hash160


@public
def Main(test: str) -> bytes:
    return hash160(test)
