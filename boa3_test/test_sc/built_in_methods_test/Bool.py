from typing import Any

from boa3.builtin import public


@public
def main(x: Any) -> bool:
    return bool(x)