from boa3.sc.compiletime import public
from boa3.sc.utils import to_bytes


@public
def len_1(int_value: int) -> bytes:
    return to_bytes(int_value, 1)


@public
def len_2(int_value: int) -> bytes:
    return to_bytes(int_value, 2)
