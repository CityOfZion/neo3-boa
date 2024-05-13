from boa3.sc.compiletime import public


@public
def Main(a: int, b: int) -> int:
    d = 1; e = 2; c = a + b
    return c
