from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator


@public
def concat_iterators(x: list) -> Iterator:
    it1 = Iterator(x)

    return it1.concat(42)
