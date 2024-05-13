from boa3.sc.compiletime import public


@public
def Main(a: bool, b: bool) -> bool:
    return a and b
