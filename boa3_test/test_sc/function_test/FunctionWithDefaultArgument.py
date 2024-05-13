from boa3.sc.compiletime import public


@public
def Main() -> list[int]:
    x = add(1, 2, 3)
    y = add(5, 6)
    return [x, y]


def add(a: int, b: int, c: int = 0) -> int:
    return a + b + c
