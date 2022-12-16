from boa3.builtin.compile_time import public
from boa3.builtin.type import UInt256


@public
def main() -> UInt256:
    bytes_value = b'0123456789abcdefghijklmnopqrstuvwxyz'
    len32 = bytes_value[:32]
    return UInt256(len32)
