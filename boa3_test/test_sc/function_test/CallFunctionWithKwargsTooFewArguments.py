def Main() -> int:
    return calc(10, c=9, d=12)


def calc(a: int, b: int, c: int = 0, d: int = 0) -> int:
    return -a + b - c + d
