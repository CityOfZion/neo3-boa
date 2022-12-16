from boa3.builtin.compile_time import public


@public
def main() -> int:
    return calc(x1=1, x2=2, x3=3, x4=4)


def calc(*, x1: int = 1, x2: int = 2, x3: int = 3, x4: int = 4) -> int:
    return x1 * 1000 + x2 * 100 + x3 * 10 + x4
