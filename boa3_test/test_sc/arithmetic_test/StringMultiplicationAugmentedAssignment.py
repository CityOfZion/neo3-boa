from boa3.builtin import public


@public
def Main(a: str, b: int) -> str:
    a *= b
    return a
