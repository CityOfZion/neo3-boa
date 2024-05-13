from boa3.sc.compiletime import public


@public
def Main(a: bool, b: bool, c: bool) -> bool:
    return a or b or c
