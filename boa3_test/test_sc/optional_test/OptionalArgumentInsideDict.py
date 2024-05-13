from typing import Optional

from boa3.sc.compiletime import public


@public
def main(a: dict[str, Optional[int]]) -> dict:
    return a
