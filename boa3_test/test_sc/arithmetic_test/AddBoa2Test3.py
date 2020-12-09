from boa3.builtin import public


@public
def main() -> int:
    a = 1
    b = 2
    c = 3
    e = 4
    d = a + b - c * e

    return d
