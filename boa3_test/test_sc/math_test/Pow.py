import math

from boa3.builtin import public


@public
def main(x: int, y: int) -> int:
    return math.pow(x, y)
