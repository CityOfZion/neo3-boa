from boa3.sc.compiletime import public


@public
def Main() -> str:
    a: int = 0
    b: str = ''

    for x in '3515':
        a = a + 1
        b = x

    return b
