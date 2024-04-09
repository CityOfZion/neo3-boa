from typing import Any

from boa3.builtin.compile_time import public


@public
def main(a: tuple, value: Any, start: int, end: int) -> int:
    return a.index(value, start, end)
