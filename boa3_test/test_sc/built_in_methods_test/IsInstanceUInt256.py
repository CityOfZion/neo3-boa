from boa3.sc.compiletime import public
from boa3.sc.types import UInt256


@public
def main(value: bytes) -> bool:
    if len(value) == 32:
        value = UInt256(value)

    return isinstance(value, UInt256)
