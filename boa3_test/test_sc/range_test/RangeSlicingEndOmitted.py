from boa3.sc.compiletime import public


@public
def Main() -> range:
    a = range(6)
    return a[2:]   # expect range(2, 6)
