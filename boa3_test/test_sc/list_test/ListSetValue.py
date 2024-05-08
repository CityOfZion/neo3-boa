from boa3.builtin.compile_time import public


@public
def Main(a: list[int]) -> list:
    a[0] = 1
    return a
