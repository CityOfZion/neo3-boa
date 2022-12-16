from boa3.builtin.compile_time import public
from boa3.builtin.type import UInt256


@public
def uint256(arg: bytes) -> bytes:
    return UInt256(arg)
