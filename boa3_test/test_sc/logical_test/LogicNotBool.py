from boa3.builtin.compile_time import public


@public
def Main(a: bool) -> int:
    return ~a
