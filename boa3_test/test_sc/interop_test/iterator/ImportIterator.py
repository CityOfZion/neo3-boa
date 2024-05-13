from boa3.sc.compiletime import public
from boa3.sc.utils import Iterator
from boa3.sc.storage import find


@public
def return_iterator() -> Iterator:
    return find(b'random_prefix')
