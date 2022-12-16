from boa3.builtin.compile_time import public


@public
def Main() -> range:
    a = range(6)
    return a[:]   # expect range(6)
