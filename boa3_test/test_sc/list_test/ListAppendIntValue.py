from typing import List

from boa3.builtin.compile_time import public


@public
def Main() -> List[int]:
    a = [1, 2, 3]
    a.append(4)
    return a
