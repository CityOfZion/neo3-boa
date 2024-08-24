from boa3.sc.compiletime import public


@public
def Main(a: int) -> int:
    assert a > 0, [0, 1, 2, 3, 4]
    return a
