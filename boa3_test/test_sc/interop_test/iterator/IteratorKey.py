from typing import Any, Dict, Union

from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator


@public
def list_iterator(x: list) -> Union[int, None]:
    it = Iterator(x)
    if it.next():
        return it.key
    return None


@public
def dict_iterator(x: Dict[int, Any]) -> Union[int, None]:
    it = Iterator(x)
    if it.next():
        return it.key
    return None
