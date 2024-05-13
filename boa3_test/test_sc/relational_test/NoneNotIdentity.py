from typing import Any

from boa3.sc.compiletime import public


@public
def main(a: Any) -> bool:
    return a is not None
