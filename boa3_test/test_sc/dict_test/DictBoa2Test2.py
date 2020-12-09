from typing import Dict, Any

from boa3.builtin import public


@public
def Main() -> int:

    d: Dict[Any, int] = {}

    d['a'] = 4
    d[13] = 3

    return d['a'] + d[13]
