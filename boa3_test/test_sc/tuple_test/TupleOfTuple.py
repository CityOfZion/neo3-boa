from boa3.sc.compiletime import public


@public
def Main(a: tuple[tuple[int, ...], ...]) -> int:
    return a[0][0]
