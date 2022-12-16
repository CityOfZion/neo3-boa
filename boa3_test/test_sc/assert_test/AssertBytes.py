from boa3.builtin.compile_time import public


@public
def Main(a: bytes) -> bytes:
    assert a
    return a
