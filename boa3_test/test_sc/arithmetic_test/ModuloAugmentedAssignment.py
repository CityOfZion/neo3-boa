from boa3.builtin import public


@public
def mod(a: int, b: int) -> int:
    a %= b
    return a
