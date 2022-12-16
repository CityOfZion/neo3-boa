from typing import Union

from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import find


@public
def test_iterator(prefix: str) -> Union[tuple, None]:
    it = find(prefix)
    if it.next():
        return it.value
    return None
