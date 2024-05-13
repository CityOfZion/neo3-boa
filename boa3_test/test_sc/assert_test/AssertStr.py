from boa3.sc.compiletime import public


@public
def Main(a: str) -> str:
    assert a
    return a
