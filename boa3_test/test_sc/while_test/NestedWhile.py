from boa3.builtin.compile_time import public


@public
def Main() -> int:
    c = 0
    d = c

    while c % 3 < 2:
        c = c + 2
        while d % 10 < 5:
            d = d + 3

        c = c + d

    return c
