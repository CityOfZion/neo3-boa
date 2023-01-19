from boa3.builtin.compile_time import public
from boa3.builtin.type import ECPoint


@public
def ecpoint_method(arg: ECPoint) -> bytes:
    return arg + b'123'
