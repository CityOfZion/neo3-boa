from boa3.builtin.compile_time import public
from boa3.builtin.type import UInt256


@public
def main() -> UInt256:
    return UInt256(256)
