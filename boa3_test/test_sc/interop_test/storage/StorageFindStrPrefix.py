from typing import Union

from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.interop.storage import find, put


def find_by_prefix(prefix: str) -> Iterator:
    return find(prefix)


def put_on_storage(key: bytes, value: Union[bytes, int, str]):
    put(key, value)
