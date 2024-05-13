from boa3.sc.compiletime import public
from boa3.sc.utils.iterator import Iterator
from boa3.sc.storage import find


@public
def find_by_prefix(prefix: int) -> Iterator:
    return find(prefix)
