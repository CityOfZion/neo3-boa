from boa3.sc.compiletime import public
from boa3.sc.utils import to_bytes


class Example:
    NUM1 = 1
    NUM2 = 2


@public
def len_1(int_value: int) -> bytes:
    return to_bytes(int_value, Example.NUM1)


@public
def len_2(int_value: int) -> bytes:
    return to_bytes(int_value, Example.NUM2)
