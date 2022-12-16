from boa3.builtin.compile_time import public


@public
def Main() -> int:
    a = (1, 2, 3)
    b = len(a)
    return b
