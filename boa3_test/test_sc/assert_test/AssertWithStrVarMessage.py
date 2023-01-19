from boa3.builtin.compile_time import public


@public
def Main(a: int) -> int:
    message = 'a must be greater than zero'
    assert a > 0, message
    return a
