from boa3.builtin import math
from boa3.builtin.compile_time import public


@public
def main(x: int) -> int:
    return math.sqrt(x)
