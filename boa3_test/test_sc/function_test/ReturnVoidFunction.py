from typing import Any

from boa3.sc.compiletime import public


@public
def Main() -> Any:
    return TestFunction()


def TestFunction():
    a = 1
