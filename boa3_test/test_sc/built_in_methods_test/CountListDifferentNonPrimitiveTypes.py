from typing import Tuple, List, Any

from boa3.builtin import public


@public
def main() -> Tuple[int, int, int]:
    a: List[Any] = [[b'unit', 'test'], [b'unit', b'unit'], [123, 123], [True, False], [True, False]]
    b: Tuple[int, int, int] = (a.count([b'unit', 'test']), a.count([123, 123]), a.count([True, False]))
    return b
