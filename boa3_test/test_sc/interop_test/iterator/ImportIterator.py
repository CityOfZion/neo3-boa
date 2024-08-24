from boa3.sc.compiletime import public
from boa3.sc.storage import find
from boa3.sc.utils import Iterator


@public
def return_iterator() -> Iterator:
    return find(b'random_prefix')
