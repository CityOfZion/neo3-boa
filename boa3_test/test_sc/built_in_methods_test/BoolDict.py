from typing import Any, Dict

from boa3.builtin import public


@public
def main(x: Dict[Any, Any]) -> bool:
    return bool(x)
