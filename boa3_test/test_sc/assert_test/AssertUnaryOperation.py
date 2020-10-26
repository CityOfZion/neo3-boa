from boa3.builtin import public


@public
def Main(a: bool, b: int) -> int:
    assert not a
    return b
