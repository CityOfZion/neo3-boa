import math

from boa3.sc.compiletime import public


@public
def main(x: int, y: int) -> int:
    return math.pow(x, y)
