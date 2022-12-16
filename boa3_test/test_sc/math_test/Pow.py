import math

from boa3.builtin.compile_time import public


@public
def main(x: int, y: int) -> int:
    return math.pow(x, y)
