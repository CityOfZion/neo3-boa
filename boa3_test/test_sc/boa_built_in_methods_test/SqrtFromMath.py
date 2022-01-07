from boa3.builtin import math, public


@public
def main(x: int) -> int:
    return math.sqrt(x)
