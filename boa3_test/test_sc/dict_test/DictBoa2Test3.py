from typing import Any

from boa3.builtin.compile_time import public


@public
def main() -> Any:

    d = {}

    d['a'] = 4
    d[13] = 3

    d['mydict'] = {}

    return d['mydict']
