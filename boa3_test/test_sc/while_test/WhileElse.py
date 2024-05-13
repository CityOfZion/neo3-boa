from boa3.sc.compiletime import public


@public
def Main() -> int:
    a = 0

    while False:
        a = a + 2
    else:
        a = a + 1

    return a
