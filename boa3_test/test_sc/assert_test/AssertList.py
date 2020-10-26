from boa3.builtin import public


@public
def Main(a: list) -> int:
    assert a
    return len(a)
