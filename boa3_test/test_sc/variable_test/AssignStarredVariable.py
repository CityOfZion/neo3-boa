from boa3.builtin.compile_time import public


@public
def Main(*a: int) -> int:
    c, *b = a  # not implemented, won't compile
    return c
