from boa3.builtin import public
from boa3.builtin.interop import iterator
from boa3.builtin.interop.storage import find


@public
def return_iterator() -> iterator.Iterator:
    return find('random_prefix')
