from typing import Any

from boa3.builtin.compile_time import public


@public
def main(a: list[Any]) -> reversed:
    return reversed(a)
