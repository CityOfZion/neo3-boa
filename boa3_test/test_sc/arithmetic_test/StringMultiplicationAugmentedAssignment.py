from boa3.sc.compiletime import public


@public
def Main(a: str, b: int) -> str:
    a *= b
    return a
