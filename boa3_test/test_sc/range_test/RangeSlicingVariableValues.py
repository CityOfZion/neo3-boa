from boa3.builtin.compile_time import public


@public
def Main() -> range:
    a1 = 2
    a2 = 3
    a = range(6)
    return a[a1:a2]   # expect range(2, 3)
