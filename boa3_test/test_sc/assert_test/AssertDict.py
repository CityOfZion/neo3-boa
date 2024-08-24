from boa3.sc.compiletime import public


@public
def Main(a: dict) -> int:
    assert a
    return len(a)
