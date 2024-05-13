from boa3.sc.compiletime import public


@public
def Main(c: int) -> int:
    a = 0

    if c < 10:
        a = a + 2

    return a
