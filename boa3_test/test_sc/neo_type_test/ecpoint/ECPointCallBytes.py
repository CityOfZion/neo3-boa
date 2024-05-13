from boa3.sc.compiletime import public
from boa3.sc.types import ECPoint


@public
def ecpoint(arg: bytes) -> ECPoint:
    return ECPoint(arg)
