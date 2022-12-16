from boa3.builtin.compile_time import public


@public
def Main(condition: bool) -> int:
    a = 0

    if condition:
        a = a + 2
    else:
        a = 10

    return a
