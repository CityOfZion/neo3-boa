from boa3.builtin import public


@public
def Main(*a: int) -> int:
    c, *b = a  # not implemented, won't compile
    return c
