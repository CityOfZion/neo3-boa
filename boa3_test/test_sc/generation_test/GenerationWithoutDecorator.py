from boa3.sc.compiletime import public


@public
def Main(a: int, b: int) -> int:
    return a + b


def Add(a: int, b: int) -> int:
    return a + b


def Sub(a: int, b: int) -> int:
    return a - b
