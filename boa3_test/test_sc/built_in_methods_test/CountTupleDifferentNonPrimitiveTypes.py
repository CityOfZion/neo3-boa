from typing import Tuple, Any

from boa3.builtin import public


@public
def main() -> Tuple[int, int, int]:
    a: Tuple[Any] = ([b'unit', 'test'], [b'unit', b'unit'], [123, 123], [True, False], [True, False])
    b: Tuple[int, int, int] = a.count([b'unit', 'test']), a.count([123, 123]), a.count([True, False])
    return b
