def Main() -> int:
    return calc(2, a=10, b=20)


def calc(a: int, b: int, c: int = 0, d: int = 0) -> int:
    return -a + b - c + d
