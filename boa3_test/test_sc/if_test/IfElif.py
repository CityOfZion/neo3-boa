from boa3.builtin.compile_time import public


@public
def Main(condition: bool) -> int:
    a = 0

    if condition:
        a = a + 2
    elif condition:
        a = 10

    return a
