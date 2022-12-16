from boa3.builtin.compile_time import public


@public
def main() -> int:

    a = 1

    b = 10

    c = 20

    d = add(a, b, 10)

    d2 = add(d, d, d)

    return d2


def add(a: int, b: int, c: int) -> int:

    result = a + b + c

    return result
