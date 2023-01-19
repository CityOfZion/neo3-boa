from boa3.builtin.compile_time import public


@public
def Main() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[3:1]   # expect []
