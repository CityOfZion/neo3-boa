from boa3.sc.compiletime import public
from boa3.sc.utils import to_bytes


@public
def main(int_value: int, length: int, big_endian: bool, signed: bool) -> bytes:
    return to_bytes(int_value, length, big_endian, signed)
