from boa3.builtin import public


@public
def Main(enter: int) -> int:
    x = enter
    while x < 10:
        x += 1
        return x
    else:
        return x
