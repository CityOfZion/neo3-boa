from typing import Any

from boa3.builtin.compile_time import public


class Example:
    def __init__(self):
        self.number = 1


@public
def test() -> Any:
    number = 10
    x = Example()
    x.number = number
    return x
