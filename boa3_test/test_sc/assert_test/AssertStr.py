from boa3.builtin import public


@public
def Main(a: str) -> str:
    assert a
    return a
