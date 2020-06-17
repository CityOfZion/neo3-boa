def Main(operation: str, args: tuple) -> int:
    a = 1
    b = 2
    return TestAdd(a, b)


def TestAdd(a: int, b: int) -> int:
    return a + b
