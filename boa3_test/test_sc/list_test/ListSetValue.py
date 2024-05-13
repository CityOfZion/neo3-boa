from boa3.sc.compiletime import public


@public
def Main(a: list[int]) -> list:
    a[0] = 1
    return a
