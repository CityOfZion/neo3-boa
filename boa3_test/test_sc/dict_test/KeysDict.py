from typing import Dict, Sequence

from boa3.builtin import public


@public
def Main() -> Sequence[str]:
    a: Dict[str, int] = {'one': 1, 'two': 2, 'three': 3}
    b = a.keys()  # expected ['one', 'two', 'three']
    return b
