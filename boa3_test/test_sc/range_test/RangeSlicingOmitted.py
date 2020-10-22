from boa3.builtin import public


@public
def Main() -> range:
    a = range(6)
    return a[:]   # expect range(6)
