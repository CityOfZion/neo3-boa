from typing import Any, Dict

from boa3.builtin.compile_time import public


@public
def main() -> Dict[Any, int]:
    d: Dict[Any, int] = {}
    d['a'] = 4
    d[13] = 3

    return d
