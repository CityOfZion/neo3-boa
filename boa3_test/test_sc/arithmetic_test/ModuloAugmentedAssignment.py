from boa3.sc.compiletime import public


@public
def mod(a: int, b: int) -> int:
    a %= b
    return a
