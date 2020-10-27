from boa3.builtin import public


@public
def Main() -> int:
    a: int = 0

    for x in (3, 5, 15):
        a = a + x

    return a
