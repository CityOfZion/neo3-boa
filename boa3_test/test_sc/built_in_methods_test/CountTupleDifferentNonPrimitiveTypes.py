from typing import Any, Tuple

from boa3.builtin.compile_time import public


@public
def main() -> Tuple[int, int, int]:
    a: Tuple[Any] = ([b'unit', 'test'], [b'unit', b'unit'], [123, 123], [True, False], [True, False])

    count1 = a.count([b'unit', 'test'])
    count2 = a.count([123, 123])
    count3 = a.count([True, False])

    b: Tuple[int, int, int] = (count1, count2, count3)
    return b
