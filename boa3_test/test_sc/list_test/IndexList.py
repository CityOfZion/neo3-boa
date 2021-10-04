from typing import Any, List

from boa3.builtin import public


@public
def main(a: List[Any], value: Any, start: int, end: int) -> int:
    return a.index(value, start, end)
