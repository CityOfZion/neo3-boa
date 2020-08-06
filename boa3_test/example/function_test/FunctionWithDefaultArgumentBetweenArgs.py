def Main():
    add(1, 2, 3)
    add(5, 6)


def add(a: int, b: int, c: int = 0, d: int) -> int:
    return a + b + c
