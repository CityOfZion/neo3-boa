from boa3.sc.compiletime import public


@public
def Main() -> int:
    x = (True, 1, 'ok')
    return x[1]

