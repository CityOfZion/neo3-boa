from boa3.sc.compiletime import public
from boa3.sc.utils.iterator import Iterator


@public
def new_iterator() -> Iterator:
    return Iterator()  # shouldn't compile
