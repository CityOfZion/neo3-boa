from boa3.builtin.compile_time import public


@public
def main(b1: int, b2: int) -> int:

    q = 4

    c2 = add_things(b1, b2)

    return q + c2


def add_things(a: int, b: int) -> int:

    result = a + b

    return result
