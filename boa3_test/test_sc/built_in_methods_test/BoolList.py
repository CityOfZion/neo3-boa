from typing import Any

from boa3.builtin.compile_time import public


@public
def main(x: list[Any]) -> bool:
    return bool(x)
