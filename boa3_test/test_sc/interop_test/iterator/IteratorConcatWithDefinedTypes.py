from typing import Dict, List

from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator


@public
def concat_iterators(x: List[str], y: Dict[int, bool]) -> Iterator:
    it1 = Iterator(x)
    it2 = Iterator(y)

    return it1.concat(it2)


@public
def concat_and_get_result(x: List[str], y: Dict[int, bool]) -> dict:
    new_map: dict = {}
    it = concat_iterators(x, y)

    while it.next():
        k = it.key
        v = it.value
        new_map[k] = v

    return new_map
