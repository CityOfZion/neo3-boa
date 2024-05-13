from typing import Any

from boa3.sc.compiletime import public


@public
def main() -> tuple[int, int, int, int]:
    a: list[list[Any]] = [[b'unit', b'unit'], [123, 123], [True, False], [True, False], [b'unit', 'test']]

    count1 = a.count([b'unit', 'test'])
    count2 = a.count([123, 123])
    count3 = a.count([True, False])
    count4 = a.count(['random value', 'random value', 'random value'])

    b: tuple[int, int, int, int] = (count1, count2, count3, count4)
    return b
