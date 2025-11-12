from boa3.sc.compiletime import public
from boa3.sc.utils import to_int


@public
def bytes_to_int_big_endian() -> int:
    return to_int(b'\x01', big_endian=False)


@public
def bytes_to_int_signed() -> int:
    return to_int(b'\x01', signed=True)


@public
def bytes_to_int_all_kwargs() -> int:
    return to_int(b'\x01', big_endian=False, signed=False)
