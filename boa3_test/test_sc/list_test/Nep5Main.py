from typing import Any, List

from boa3.builtin.compile_time import public


@public
def Main(operation: str, args: List[Any]) -> Any:
    return args[0]
