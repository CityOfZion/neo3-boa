def Main(operation: str, args: tuple) -> bool:
    a = 1
    b = 2
    TestAdd(a, b)
    return True


def TestAdd(a: int, b: int):
    c = a + b
