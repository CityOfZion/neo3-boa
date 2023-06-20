from boa3.builtin import interop
from boa3.builtin.compile_time import public


@public
def return_iterator() -> interop.iterator.Iterator:
    return interop.storage.find(b'random_prefix')
