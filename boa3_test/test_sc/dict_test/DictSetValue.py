from boa3.sc.compiletime import public


@public
def Main(a: dict[int, str]) -> dict[int, str]:
    a[0] = 'ok'
    return a
