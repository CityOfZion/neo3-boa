from boa3.builtin import interop, public


@public
def return_iterator() -> interop.iterator.Iterator:
    return interop.storage.find('random_prefix')
