from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.interop.storage import find


@public
def is_iterator(value: Any) -> bool:
    return isinstance(value, Iterator)


@public
def storage_find_is_context() -> bool:
    storage_find_iterator = find('unit_test')
    return is_iterator(storage_find_iterator)
