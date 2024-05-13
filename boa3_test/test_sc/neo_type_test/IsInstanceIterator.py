from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.storage import find
from boa3.sc.utils.iterator import Iterator


@public
def is_iterator(value: Any) -> bool:
    return isinstance(value, Iterator)


@public
def storage_find_is_context() -> bool:
    storage_find_iterator = find(b'unit_test')
    return is_iterator(storage_find_iterator)
