from boa3.sc.compiletime import public


@public
def Main() -> int:
    a = 0
    sequence = (3, 5, 15)

    for x in sequence:
        if x % 5 != 0:
            continue

        a = a + x

    return a
