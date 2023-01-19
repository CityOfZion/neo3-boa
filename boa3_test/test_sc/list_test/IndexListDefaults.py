from typing import Any, List

from boa3.builtin.compile_time import public


@public
def main(a: List[Any], value: Any) -> int:
    return a.index(value)
