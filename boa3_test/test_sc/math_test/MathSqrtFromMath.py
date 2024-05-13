from math import sqrt

from boa3.sc.compiletime import public


@public
def main(x: int) -> int:
    return sqrt(x)
