from boa3.sc.compiletime import public
from boa3.sc.types import ECPoint


@public
def ecpoint_method(arg: ECPoint) -> bytes:
    return arg + b'123'
