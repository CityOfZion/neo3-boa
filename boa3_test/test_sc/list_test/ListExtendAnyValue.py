from typing import Any

from boa3.sc.compiletime import public


@public
def Main() -> list[Any]:
    a: list[Any] = [1, 2, 3]
    a.extend(('4', 5, True))
    return a  # expected [1, 2, 3, '4', 5, True]
