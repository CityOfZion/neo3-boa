from boa3.sc.compiletime import public


@public
def Main(value: int) -> int:
    a = 0
    condition = a < value

    while condition:
        a = a + 2
        condition = a < value * 2

    return a
