from boa3.sc.compiletime import public


@public
def Main() -> int:
    a = 0
    b = 0

    while b < 10:
        a = a + 2
        b = b + 1

    return a
