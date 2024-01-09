from boa3.builtin.compile_time import public


@public
def left_shift(a: int, b: int) -> int:
    a <<= b
    return a


@public
def right_shift(a: int, b: int) -> int:
    a >>= b
    return a


@public
def l_and(a: int, b: int) -> int:
    a &= b
    return a


@public
def l_or(a: int, b: int) -> int:
    a |= b
    return a


@public
def xor(a: int, b: int) -> int:
    a ^= b
    return a
