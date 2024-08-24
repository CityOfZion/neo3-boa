from typing import Any

from boa3.sc.compiletime import public


@public
def Main() -> Any:
    a = 1
    b = 2
    c = DoSomething()
    return c


def DoSomething():
    pass
