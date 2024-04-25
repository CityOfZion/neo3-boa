from boa3.builtin.compile_time import public
from boa3.builtin.interop import iterator
from boa3.sc.storage import find


@public
def return_iterator() -> iterator.Iterator:
    return find(b'random_prefix')
