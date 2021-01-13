from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator


@public
def concat_iterators(x: list, y: dict) -> Iterator:
    it1 = Iterator(x)
    it2 = Iterator(y)

    return it1.concat(it2)


@public
def concat_and_get_result(x: list, y: dict) -> dict:
    new_map = {}
    it = concat_iterators(x, y)

    while it.next():
        k = it.key
        v = it.value
        new_map[k] = v

    return new_map
