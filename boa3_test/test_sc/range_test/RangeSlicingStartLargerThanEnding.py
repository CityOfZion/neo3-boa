from boa3.builtin.compile_time import public


@public
def Main() -> range:
    a = range(6)
    return a[3:2]   # expect range(3, 2)
