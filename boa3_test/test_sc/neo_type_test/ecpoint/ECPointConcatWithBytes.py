from boa3.builtin import public
from boa3.builtin.type import ECPoint


@public
def ecpoint_method(arg: ECPoint) -> bytes:
    return arg + b'123'