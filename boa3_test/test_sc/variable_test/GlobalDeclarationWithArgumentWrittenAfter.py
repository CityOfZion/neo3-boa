from boa3.builtin.compile_time import public

a: int


@public
def Main() -> int:
    return a


a = 10
