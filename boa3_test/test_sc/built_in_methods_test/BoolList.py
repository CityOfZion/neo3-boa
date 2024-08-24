from typing import Any

from boa3.sc.compiletime import public


@public
def main(x: list[Any]) -> bool:
    return bool(x)
