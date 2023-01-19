from typing import List

from boa3.builtin.compile_time import public


@public
def Main() -> List[int]:
    a = [1, 2, 3]
    list.extend(a, [4, 5, 6])
    return a  # expected [1, 2, 3, 4, 5, 6]
