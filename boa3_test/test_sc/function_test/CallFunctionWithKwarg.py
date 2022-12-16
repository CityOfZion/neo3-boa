from boa3.builtin.compile_time import public


@public
def Main(n: int) -> int:
    return negate(number=n)


def negate(number: int) -> int:
    return -number
