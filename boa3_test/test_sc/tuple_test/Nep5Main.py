from typing import Any, Tuple

from boa3.builtin import public


@public
def Main(operation: str, args: Tuple[Any]) -> Any:
    return args[0]
