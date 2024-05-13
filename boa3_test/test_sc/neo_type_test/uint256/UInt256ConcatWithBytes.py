from boa3.sc.compiletime import public
from boa3.sc.types import UInt256


@public
def uint256_method(arg: UInt256) -> bytes:
    return arg + b'123'
