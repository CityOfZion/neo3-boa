from boa3.sc.compiletime import public


@public
def Main(a: str, b: str) -> bool:
    return a != b
