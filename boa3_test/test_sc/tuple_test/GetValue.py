from boa3.builtin.compile_time import public


@public
def Main(a: tuple[int, ...]) -> int:
    return a[0]
