from typing import Union

from boa3.builtin.compile_time import public
from boa3.builtin.interop import storage


@public
def test_iterator(prefix: bytes) -> Union[tuple, None]:
    it = storage.find(prefix)
    if it.next():
        return it.value
    return None


@public
def store_data(key: bytes, value: int):
    storage.put(key, value)
