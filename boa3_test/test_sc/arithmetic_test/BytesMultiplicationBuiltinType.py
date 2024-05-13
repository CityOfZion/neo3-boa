from boa3.sc.compiletime import public
from boa3.sc.types import FindOptions


@public
def bytes_mult(a: bytes, b: FindOptions) -> bytes:
    return a * b
