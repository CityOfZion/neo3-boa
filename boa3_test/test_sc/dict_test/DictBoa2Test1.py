from typing import Any

from boa3.builtin.compile_time import public


@public
def main() -> dict[Any, int]:
    d: dict[Any, int] = {}
    d['a'] = 4
    d[13] = 3

    return d
