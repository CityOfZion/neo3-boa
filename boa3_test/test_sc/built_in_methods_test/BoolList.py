from typing import Any, List

from boa3.builtin.compile_time import public


@public
def main(x: List[Any]) -> bool:
    return bool(x)
