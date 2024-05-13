from boa3.sc.compiletime import public
from boa3.sc.types import UInt160


@public
def uint160(arg: bytes) -> bytes:
    return UInt160(arg)
