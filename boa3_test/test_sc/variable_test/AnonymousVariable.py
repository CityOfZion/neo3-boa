from boa3.sc.compiletime import public


@public
def Main() -> int:
    x = 0
    for _ in range(20):
        x += 10

    for _ in '0123456789':
        x += 20

    return x
