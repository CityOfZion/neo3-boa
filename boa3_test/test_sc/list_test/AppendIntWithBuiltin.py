from typing import List

from boa3.builtin import public


@public
def Main() -> List[int]:
    a = [1, 2, 3]
    list.append(a, 4)
    return a
