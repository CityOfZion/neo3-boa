from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator


@public
def new_iterator() -> Iterator:
    return Iterator()  # shouldn't compile
