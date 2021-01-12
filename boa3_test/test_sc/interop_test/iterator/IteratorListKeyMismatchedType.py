from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator


@public
def list_iterator(x: list) -> str:
    it = Iterator(x)
    it.next()
    return it.key
