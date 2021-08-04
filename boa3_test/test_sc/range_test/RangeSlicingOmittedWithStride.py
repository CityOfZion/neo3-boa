from boa3.builtin import public


@public
def Main() -> range:
    a = range(6)
    return a[::2]   # expect range(0, 6, 2)
