from typing import Tuple

from boa3.builtin.compile_time import public


class Example:
    @staticmethod
    def test() -> int:
        return 10


@public
def test() -> int:
    return 20


@public
def result() -> Tuple[int, int]:
    a = Example.test()
    b = test()
    c = (a, b)
    return c
