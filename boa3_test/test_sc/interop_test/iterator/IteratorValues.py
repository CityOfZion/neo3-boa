from typing import Any, Dict, List, Union

from boa3.builtin import public
from boa3.builtin.interop.enumerator import Enumerator
from boa3.builtin.interop.iterator import Iterator


@public
def list_iterator(x: List[int]) -> Union[Enumerator, None]:
    it = Iterator(x)
    if it.next():
        return it.values()
    return None


@public
def dict_iterator(x: Dict[Any, int]) -> Union[Enumerator, None]:
    it = Iterator(x)
    if it.next():
        return it.values()
    return None
