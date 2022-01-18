from typing import Any, List

from boa3.builtin import public


@public
def main(x: List[Any]) -> bool:
    return bool(x)
