from typing import Any, Dict

from boa3.builtin.compile_time import public


@public
def Main():
    a: Dict[int, Any] = {
        1: True,
        2: 4,
        3: 'nine'
    }
