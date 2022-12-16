from typing import Any, List, Tuple

from boa3.builtin.compile_time import public


@public
def main() -> Tuple[int, int, int, int]:
    a: List[Any] = [[b'unit', b'unit'], [123, 123], [True, False], [True, False], [b'unit', 'test'], 'not list']

    count1 = a.count([b'unit', 'test'])
    count2 = a.count([123, 123])
    count3 = a.count([True, False])
    count4 = a.count(['random value', 'random value', 'random value'])

    b: Tuple[int, int, int, int] = (count1, count2, count3, count4)
    return b
