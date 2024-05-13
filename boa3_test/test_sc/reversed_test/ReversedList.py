from typing import Any

from boa3.sc.compiletime import public


@public
def main(a: list[Any]) -> reversed:
    return reversed(a)
