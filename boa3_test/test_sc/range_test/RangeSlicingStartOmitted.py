from boa3.sc.compiletime import public


@public
def Main() -> range:
    a = range(6)
    return a[:3]   # range(0, 3)
