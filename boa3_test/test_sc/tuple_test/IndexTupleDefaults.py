from typing import Any

from boa3.sc.compiletime import public


@public
def main(a: tuple, value: Any) -> int:
    return a.index(value)
