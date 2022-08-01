from typing import Tuple

from boa3.builtin import public


@public
def main() -> Tuple[int, int, int]:
    a = [b'unit', 'test', b'unit', b'unit', 123, 123, True, False]
    b: Tuple[int, int, int] = (a.count(b'unit'), a.count('test'), a.count(123))
    return b
