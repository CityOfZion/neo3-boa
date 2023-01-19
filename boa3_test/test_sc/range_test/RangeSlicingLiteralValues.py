from boa3.builtin.compile_time import public


@public
def Main() -> range:
    a = range(6)
    return a[2:3]   # expect range(2, 3)
