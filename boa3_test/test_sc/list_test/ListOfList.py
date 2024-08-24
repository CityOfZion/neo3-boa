from boa3.sc.compiletime import public


@public
def Main(a: list[list[int]]) -> int:
    return a[0][0]
