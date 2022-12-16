from boa3.builtin.compile_time import public


@public
def Main(a: int, b: int) -> int:
    return a + b


def Add(a: int, b: int) -> int:
    return a + b


def Sub(a: int, b: int) -> int:
    return a - b
