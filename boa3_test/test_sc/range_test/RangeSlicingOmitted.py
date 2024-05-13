from boa3.sc.compiletime import public


@public
def Main() -> range:
    a = range(6)
    return a[:]   # expect range(6)
