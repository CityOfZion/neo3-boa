from boa3.sc.compiletime import public


@public
def Main() -> range:
    a = range(6)
    return a[3:2]   # expect range(3, 2)
