from boa3.builtin.compile_time import public

b: int = 0


@public
def Main(a: int) -> int:
    b = a
    return b
