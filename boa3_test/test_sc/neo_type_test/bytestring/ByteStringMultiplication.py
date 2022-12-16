from boa3.builtin.compile_time import public
from boa3.builtin.type import ByteString


@public
def bytestring_mult(a: ByteString, b: int) -> ByteString:
    return a * b
