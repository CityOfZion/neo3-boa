from boa3.builtin.compile_time import public


@public
def Main(c: int) -> int:
    a = 0

    if c < 10:
        a = a + 2

    return a
