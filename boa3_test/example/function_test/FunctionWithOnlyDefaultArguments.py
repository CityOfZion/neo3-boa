def Main():
    add()
    add(5, 6)
    add(9)
    add(1, 2, 3)


def add(a: int = 0, b: int = 0, c: int = 0) -> int:
    return a + b + c
