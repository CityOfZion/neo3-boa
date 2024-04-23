from boa3.builtin.compile_time import public


@public
def Main(a: list[list[int]]) -> int:
    return a[0][0]
