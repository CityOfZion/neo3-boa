from boa3.builtin import public


@public
def Main() -> int:
    a = 0

    while False:
        a = a + 2

    return a
