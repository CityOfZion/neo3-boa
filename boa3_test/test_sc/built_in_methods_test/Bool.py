from typing import Any

from boa3.sc.compiletime import public


@public
def main(x: Any) -> bool:
    return bool(x)
