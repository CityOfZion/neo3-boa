from boa3.builtin import public
from boa3.builtin.math import sqrt


@public
def main(x: int) -> int:
    return sqrt(x)
