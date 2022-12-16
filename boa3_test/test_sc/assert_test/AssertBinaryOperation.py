from boa3.builtin.compile_time import public


@public
def Main(a: int, b: int) -> int:
    assert a != b
    return a
