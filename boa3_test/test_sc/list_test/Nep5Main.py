from typing import Any, List

from boa3.builtin import public


@public
def Main(operation: str, args: List[Any]) -> Any:
    return args[0]
