from typing import List

from boa3.builtin.compile_time import public


@public
def Main(operation: str, args: List[int]) -> int:
    if len(args) < 2:
        return 0
    a: int = args[0]
    b: int = args[1]
    c: int
    if a < b:
        c = Add(a, b)
    elif a <= 0 and b <= 0:
        c = Sub(a, b)
    else:
        c = 0
        for x in [a, b, Add(a, b), Sub(a, b)]:
            c += a + b
    return c


def Add(a: int, b: int) -> int:
    return a + b


@public
def Sub(a: int, b: int) -> int:
    return a - b
