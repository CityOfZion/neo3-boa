from typing import Any, List

from boa3.builtin import public


@public
def Main() -> List[Any]:
    a: List[Any] = [1, 2, 3]
    a.insert(1, '4')
    return a  # expected [1, '4', 2, 3]
