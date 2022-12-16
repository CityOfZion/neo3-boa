from typing import Any

from boa3.builtin.compile_time import public


@public
def example(value: Any) -> int:
    if not isinstance(value, int):
        return -1
    else:
        return value
