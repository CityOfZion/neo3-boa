import math

from boa3.sc.compiletime import public


@public
def main(x: int) -> int:
    return math.sqrt(x)
