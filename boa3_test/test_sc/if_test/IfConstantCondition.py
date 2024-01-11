from boa3.builtin.compile_time import public


@public
def Main() -> int:
    a = 0

    if True:
        a = a + 2

    return a
