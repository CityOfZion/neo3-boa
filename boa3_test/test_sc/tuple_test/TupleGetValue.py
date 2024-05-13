from boa3.sc.compiletime import public


@public
def Main(a: tuple[int, ...]) -> int:
    return a[0]
