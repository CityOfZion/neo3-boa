from typing import Any

from boa3.sc.compiletime import public


@public
def main(a: list[Any], value: Any, start: int) -> int:
    return a.index(value, start)
