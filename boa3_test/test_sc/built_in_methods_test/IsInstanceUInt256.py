from boa3.builtin import public
from boa3.builtin.type import UInt256


@public
def main(value: bytes) -> bool:
    if len(value) == 32:
        value = UInt256(value)

    return isinstance(value, UInt256)
