from boa3.builtin.compile_time import public

a: int = 10


@public
def Main() -> int:
    return a
