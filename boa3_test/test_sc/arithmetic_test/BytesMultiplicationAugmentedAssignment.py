from boa3.sc.compiletime import public


@public
def Main(a: bytes, b: int) -> bytes:
    a *= b
    return a
