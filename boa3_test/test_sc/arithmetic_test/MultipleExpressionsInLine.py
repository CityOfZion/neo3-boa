from boa3.builtin.compile_time import public


@public
def Main(a: int, b: int) -> int:
    d = 1; e = 2; c = a + b
    return c
