from typing import Any, List

from boa3.builtin import public


@public
def Main() -> List[Any]:
    a: List[Any] = [1, 2, 3]
    a.extend(('4', 5, True))
    return a  # expected [1, 2, 3, '4', 5, True]
