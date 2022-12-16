from boa3.builtin.compile_time import public


@public
def main() -> int:
    a = 1
    b = 2
    c = 3
    e = 4
    d = a + b - c * e

    return d
