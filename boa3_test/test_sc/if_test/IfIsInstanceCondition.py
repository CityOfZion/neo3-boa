from typing import Any

from boa3.sc.compiletime import public


@public
def example(value: Any) -> int:
    if isinstance(value, int):
        return value
    return -1
