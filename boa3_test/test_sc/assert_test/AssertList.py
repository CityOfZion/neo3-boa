from boa3.sc.compiletime import public


@public
def Main(a: list) -> int:
    assert a
    return len(a)
