from typing import Dict

from boa3.builtin.compile_time import public


@public
def Main():
    a: Dict[int, int] = {1: 15, 2: 14, 3: 13}
