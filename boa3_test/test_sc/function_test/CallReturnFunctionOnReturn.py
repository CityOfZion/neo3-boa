from boa3.builtin.compile_time import public


@public
def Main() -> int:
    a = 1
    b = 2
    return TestAdd(a, b)


def TestAdd(a: int, b: int) -> int:
    return a + b
