from typing import Any, Dict

from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator


@public
def dict_iterator(x: Dict[Any, Any]) -> Iterator:
    return Iterator(x)
