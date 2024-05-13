from boa3.sc.compiletime import public


@public
def pow(a: int, b: int) -> int:
    return a ** b
