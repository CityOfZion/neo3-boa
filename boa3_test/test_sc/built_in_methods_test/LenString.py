from boa3.sc.compiletime import public


@public
def Main() -> int:
    a = 'just a test'
    return len(a)
