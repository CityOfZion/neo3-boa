from boa3.builtin import public


@public
def Main(n: int) -> int:
    return negate(number=n)


def negate(number: int) -> int:
    return -number
