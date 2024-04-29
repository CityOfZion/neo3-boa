from collections.abc import Sequence

from boa3.builtin.compile_time import public


@public
def Main() -> Sequence[str]:
    a: dict[str, int] = {'one': 1, 'two': 2, 'three': 3}
    b: tuple[str, ...] = a.keys()
    return b
