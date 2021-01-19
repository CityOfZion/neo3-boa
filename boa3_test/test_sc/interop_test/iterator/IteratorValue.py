from typing import Any, Dict, List, Tuple, Union

from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator


@public
def list_iterator(x: List[int]) -> Union[int, None]:
    it = Iterator(x)
    if it.next():
        return it.value
    return None


@public
def dict_iterator(x: Dict[Any, int]) -> Union[Tuple[Any, int], None]:
    it = Iterator(x)
    if it.next():
        return it.value
    return None
