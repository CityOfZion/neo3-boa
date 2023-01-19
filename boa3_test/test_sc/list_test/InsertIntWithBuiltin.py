from typing import List

from boa3.builtin.compile_time import public


@public
def Main() -> List[int]:
    a = [1, 2, 3]
    list.insert(a, 2, 4)
    return a  # expected [1, 2, 4, 3]
