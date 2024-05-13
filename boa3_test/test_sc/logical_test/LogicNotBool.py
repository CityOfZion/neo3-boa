from boa3.sc.compiletime import public


@public
def Main(a: bool) -> int:
    return ~a
