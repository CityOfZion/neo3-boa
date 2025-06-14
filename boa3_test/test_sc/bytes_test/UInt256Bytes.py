from boa3.sc.compiletime import public
from boa3.sc.types import UInt256


@public
def main() -> UInt256:
    bytes_value = b'0123456789abcdefghijklmnopqrstuvwxyz'
    len32 = bytes_value[:32]
    return UInt256(len32)
