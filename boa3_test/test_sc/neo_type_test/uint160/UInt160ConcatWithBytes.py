from boa3.sc.compiletime import public
from boa3.sc.types import UInt160


@public
def uint160_method(arg: UInt160) -> bytes:
    return arg + b'123'
