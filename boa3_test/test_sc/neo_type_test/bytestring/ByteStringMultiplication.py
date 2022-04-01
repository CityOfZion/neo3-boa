from boa3.builtin import public
from boa3.builtin.type import ByteString


@public
def bytestring_mult(a: ByteString, b: int) -> ByteString:
    return a * b
