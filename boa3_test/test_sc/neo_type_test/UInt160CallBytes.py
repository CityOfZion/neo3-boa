from boa3.builtin import public
from boa3.builtin.type import UInt160


@public
def uint160(arg: bytes) -> UInt160:
    return UInt160(arg)
