from boa3.sc.compiletime import public
from boa3.sc.utils import to_bytes


@public
def int_to_bytes_length() -> bytes:
    return to_bytes(12, length=1)


@public
def int_to_bytes_big_endian() -> bytes:
    return to_bytes(12, big_endian=True)


@public
def int_to_bytes_signed() -> bytes:
    return to_bytes(12, signed=False)


@public
def int_to_bytes_two_kwargs() -> bytes:
    return to_bytes(12, length=None, signed=False)


@public
def int_to_bytes_all_kwargs() -> bytes:
    return to_bytes(12, length=1, big_endian=True, signed=False)
