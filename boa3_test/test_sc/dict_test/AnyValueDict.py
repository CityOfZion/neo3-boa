from typing import Any

from boa3.builtin.compile_time import public


@public
def Main():
    a: dict[int, Any] = {
        1: True,
        2: 4,
        3: 'nine'
    }
