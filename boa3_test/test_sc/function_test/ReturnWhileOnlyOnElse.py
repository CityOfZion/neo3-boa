from boa3.sc.compiletime import public


@public
def Main(enter: int) -> int:
    x = enter
    while x < 10:
        x += 1
    else:
        return x
