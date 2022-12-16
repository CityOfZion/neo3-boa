from typing import Any

from boa3.builtin.compile_time import public


@public
def example(value: Any) -> int:
    if isinstance(value, int):
        return value
    return -1
