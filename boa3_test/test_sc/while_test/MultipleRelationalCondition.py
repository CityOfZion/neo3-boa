from boa3.builtin.compile_time import public


@public
def Main(operation: str, arg: int) -> int:
    a = 0
    b = 0

    while b < 10 < arg:
        a = a + 2
        b = b + 1

    return a
