from boa3.sc.compiletime import public
from boa3.sc.types import UInt160


@public
def uint160(arg: int) -> UInt160:
    return UInt160(arg)
