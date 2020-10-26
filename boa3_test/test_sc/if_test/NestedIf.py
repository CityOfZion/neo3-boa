from boa3.builtin import public


@public
def Main(a: bool, b: bool) -> int:
    c = 0
    d = c

    if a:
        c = c + 2
        if b:
            d = d + 3
        c = c + d

    return c
