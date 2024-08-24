from boa3.sc.compiletime import public


@public
def Main(a: bytes) -> int:
    return a[0]
