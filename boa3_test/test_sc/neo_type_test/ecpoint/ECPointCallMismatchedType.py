from boa3.builtin.compile_time import public
from boa3.builtin.type import ECPoint


@public
def ecpoint(arg: str) -> ECPoint:
    return ECPoint(arg)
