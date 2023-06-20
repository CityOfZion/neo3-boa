from typing import Union

from boa3.builtin.compile_time import public
from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.interop.storage import find, get_context, put


@public
def find_by_prefix(prefix: bytes) -> Iterator:
    context = get_context()
    return find(prefix, context)


@public
def put_on_storage(key: bytes, value: Union[bytes, int, str]):
    put(key, value)
