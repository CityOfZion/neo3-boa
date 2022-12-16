from typing import Any, Dict

from boa3.builtin.compile_time import public


@public
def main(x: Dict[Any, Any]) -> bool:
    return bool(x)
