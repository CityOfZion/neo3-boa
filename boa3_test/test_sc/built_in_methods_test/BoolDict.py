from typing import Any

from boa3.sc.compiletime import public


@public
def main(x: dict[Any, Any]) -> bool:
    return bool(x)
