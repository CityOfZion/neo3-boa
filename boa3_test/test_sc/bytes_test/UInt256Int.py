from boa3.builtin import public
from boa3.builtin.type import UInt256


@public
def main() -> UInt256:
    return UInt256(256)
