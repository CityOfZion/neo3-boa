from boa3.builtin.compile_time import public


@public
def Main(a: int) -> int:
    assert a > 0, 'a must be greater than zero'
    return a
