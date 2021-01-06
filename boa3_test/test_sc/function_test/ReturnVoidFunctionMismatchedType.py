from typing import Any

from boa3.builtin import public


@public
def Main() -> int:
    return TestFunction()


def TestFunction():
    a = 1
