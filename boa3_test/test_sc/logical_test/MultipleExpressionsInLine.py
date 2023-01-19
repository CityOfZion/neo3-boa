from boa3.builtin.compile_time import public


@public
def Main(a: bool, b: bool, c: bool) -> bool:
    a1 = a and b; b1 = b and c; c1 = a or c
    return a1 and not b1 and c1
