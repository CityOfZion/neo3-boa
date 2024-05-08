from typing import Any

from boa3.builtin.compile_time import public


@public
def main(x: dict[Any, Any]) -> bool:
    return bool(x)
