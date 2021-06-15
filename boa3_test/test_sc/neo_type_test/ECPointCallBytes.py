from boa3.builtin import public
from boa3.builtin.type import ECPoint


@public
def ecpoint(arg: bytes) -> ECPoint:
    return ECPoint(arg)
