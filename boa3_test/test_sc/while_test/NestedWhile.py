def Main(a: bool, b: bool) -> int:
    c = 0
    d = c

    while a:
        c = c + 2
        while b:
            d = d + 3
        c = c + d

    return c
