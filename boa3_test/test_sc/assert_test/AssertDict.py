from boa3.builtin.compile_time import public


@public
def Main(a: dict) -> int:
    assert a
    return len(a)
