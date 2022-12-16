from boa3.builtin.compile_time import public
from boa3.builtin.type import UInt160


@public
def main() -> UInt160:
    bytes_value = b'0123456789abcdefghijklmnopqrstuvwxyz'
    len20 = bytes_value[:20]
    return UInt160(len20)
