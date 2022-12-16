from boa3.builtin.compile_time import public
from boa3.builtin.interop.iterator import Iterator


@public
def new_iterator() -> Iterator:
    return Iterator()  # shouldn't compile
