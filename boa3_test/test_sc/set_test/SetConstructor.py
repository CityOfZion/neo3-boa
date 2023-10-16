from typing import Any

from boa3.builtin.compile_time import public


@public
def main() -> Any:
    a = ('unit', 'test')
    return set(a)
