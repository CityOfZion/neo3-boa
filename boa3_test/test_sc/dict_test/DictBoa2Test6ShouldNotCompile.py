from typing import Any

from boa3.builtin.compile_time import public


@public
def main() -> dict[Any, int]:

    q = 3

    return {'a': 1, 'b': 2}
