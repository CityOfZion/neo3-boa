from boa3.sc.compiletime import public


@public
def Main(a: bytes) -> bytes:
    assert a
    return a
