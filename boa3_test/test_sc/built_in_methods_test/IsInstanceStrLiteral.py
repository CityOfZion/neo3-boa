from boa3.sc.compiletime import public


@public
def Main() -> bool:
    return isinstance('123', str)
