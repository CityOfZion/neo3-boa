from boa3.sc.compiletime import public
from boa3.sc.types import UInt256


@public
def uint256(arg: int) -> UInt256:
    return UInt256(arg)
