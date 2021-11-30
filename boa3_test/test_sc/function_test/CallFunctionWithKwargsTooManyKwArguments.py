def Main() -> int:
    return calc(a=10, b=20, another_kwarg=999, c=30, d=40)


def calc(a: int, b: int, c: int = 0, d: int = 0) -> int:
    return -a + b - c + d
