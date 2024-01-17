from boa3.builtin.compile_time import public


@public
def Main(a: range) -> int:
    return a[0]
