from boa3.builtin.compile_time import public


@public(safe=42)
def Main(a: int, b: int) -> int:
    c = Add(a, b)
    return c


def Add(a: int, b: int) -> int:
    return a + b


@public
def Sub(a: int, b: int) -> int:
    return a - b
