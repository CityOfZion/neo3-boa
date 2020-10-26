from boa3.builtin import public


@public
def Main() -> range:
    a = range(6)
    return a[:-4]   # expect range(0, 2)
