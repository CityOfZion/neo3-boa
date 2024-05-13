from boa3.sc.compiletime import public


@public
def Main(n: int) -> int:
    return negate(number=n)


def negate(number: int) -> int:
    return -number
