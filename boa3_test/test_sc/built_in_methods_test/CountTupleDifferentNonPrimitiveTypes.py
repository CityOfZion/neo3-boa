from typing import Any

from boa3.sc.compiletime import public


@public
def main() -> tuple[int, int, int]:
    a: tuple[Any] = ([b'unit', 'test'], [b'unit', b'unit'], [123, 123], [True, False], [True, False])

    count1 = a.count([b'unit', 'test'])
    count2 = a.count([123, 123])
    count3 = a.count([True, False])

    b: tuple[int, int, int] = (count1, count2, count3)
    return b
