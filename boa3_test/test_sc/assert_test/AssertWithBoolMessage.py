from boa3.builtin import public


@public
def Main(a: int) -> int:
    assert a > 0, False
    return a
