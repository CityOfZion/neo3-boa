from boa3.builtin.compile_time import public


@public
def Main(a: bool, b: int) -> int:
    assert not a
    return b
