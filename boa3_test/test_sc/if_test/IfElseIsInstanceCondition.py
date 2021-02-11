from typing import Any

from boa3.builtin import public


@public
def example(value: Any) -> int:
    if not isinstance(value, int):
        return -1
    else:
        return value
