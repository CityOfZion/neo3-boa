from typing import List, Tuple

from boa3.builtin.compile_time import public


@public
def mixed() -> bool:
    a: List[int] = [1, 2, 3]
    b: Tuple[str, str] = ('unit', 'test')
    return a is b
