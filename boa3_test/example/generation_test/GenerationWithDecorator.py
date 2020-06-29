from boa3.builtin import public


@public
def Main(a: int, b: int) -> int:
    return a + b


def Add(a: int, b: int) -> int:
    return a + b


@public
def Sub(a: int, b: int) -> int:
    return a - b
