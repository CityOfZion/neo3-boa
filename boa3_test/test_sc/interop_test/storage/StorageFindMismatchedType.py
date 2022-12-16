from boa3.builtin.compile_time import public
from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.interop.storage import find


@public
def find_by_prefix(prefix: int) -> Iterator:
    return find(prefix)
