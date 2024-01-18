from typing import Any, List

from boa3.builtin.compile_time import public


@public
def main() -> Any:
    m: List[Any] = [1, 2, 2]
    m.append(7)
    q = [6, 7]
    l = 'howdy'
    m.append(l)
    m.append(q)
    m.append(b'\x01')
    return m[5]
