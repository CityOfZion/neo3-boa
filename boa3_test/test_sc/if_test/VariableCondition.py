from boa3.builtin import public


@public
def Main(condition: bool) -> int:
    a = 0

    if condition:
        a = a + 2

    return a
