from boa3.sc.compiletime import public
from boa3.sc.utils import to_int


@public
def main(bytes_: bytes, big_endian: bool) -> int:
    return to_int(bytes_, big_endian)
