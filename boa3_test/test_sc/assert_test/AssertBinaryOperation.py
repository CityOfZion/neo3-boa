from boa3.builtin import public


@public
def Main(a: int, b: int) -> int:
    assert a != b
    return a
