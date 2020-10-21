from boa3.builtin import public


@public
def Main(a: bytes) -> bytes:
    assert a
    return a
