from typing import Optional

from boa3.builtin.compile_time import public


@public
def main(a: dict[str, Optional[int]]) -> dict:
    return a
