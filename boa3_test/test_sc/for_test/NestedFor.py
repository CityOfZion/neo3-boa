from boa3.sc.compiletime import public


@public
def Main() -> int:
    a: int = 0
    sequence: tuple[int, int, int] = (3, 5, 15)

    for x in sequence:
        for y in sequence:
            a = a + x * y

    return a
