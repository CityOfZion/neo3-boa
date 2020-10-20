from boa3.builtin import public


def Main(operation: str, args: tuple) -> int:
    a = 1
    b = 2
    c = TestAdd(a, b)
    return c


@public
def TestAdd(a: int, b: int) -> int:
    return a + b
