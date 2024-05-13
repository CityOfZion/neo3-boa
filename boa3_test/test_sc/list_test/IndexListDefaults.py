from typing import Any

from boa3.sc.compiletime import public


@public
def main(a: list[Any], value: Any) -> int:
    return a.index(value)
