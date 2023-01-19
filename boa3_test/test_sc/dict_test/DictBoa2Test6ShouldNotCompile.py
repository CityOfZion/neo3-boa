from typing import Any, Dict

from boa3.builtin.compile_time import public


@public
def main() -> Dict[Any, int]:

    q = 3

    return {'a': 1, 'b': 2}
