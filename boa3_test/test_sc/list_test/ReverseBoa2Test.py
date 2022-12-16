from typing import Any, List

from boa3.builtin.compile_time import public


@public
def main() -> List[Any]:
    m = [1, 2, 4, 'blah']
    m.reverse()
    return m
