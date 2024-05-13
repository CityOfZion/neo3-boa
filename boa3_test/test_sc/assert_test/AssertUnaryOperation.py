from boa3.sc.compiletime import public


@public
def Main(a: bool, b: int) -> int:
    assert not a
    return b
