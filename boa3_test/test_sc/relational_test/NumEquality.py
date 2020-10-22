from boa3.builtin import public


@public
def Main(a: int, b: int) -> bool:
    return a == b
