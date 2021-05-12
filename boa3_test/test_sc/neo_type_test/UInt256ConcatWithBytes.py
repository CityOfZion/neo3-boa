from boa3.builtin import public
from boa3.builtin.type import UInt256


@public
def uint256_method(arg: UInt256) -> bytes:
    return arg + b'123'
