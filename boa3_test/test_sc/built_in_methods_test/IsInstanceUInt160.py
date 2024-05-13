from boa3.sc.compiletime import public
from boa3.sc.types import UInt160


@public
def Main(value: bytes) -> bool:
    if len(value) == 20:
        value = UInt160(value)

    return isinstance(value, UInt160)
