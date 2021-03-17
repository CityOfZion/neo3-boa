from typing import Union

from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.interop.storage import find, get_context, put


@public
def find_by_prefix(prefix: Union[str, bytes]) -> Iterator:
    context = get_context()
    return find(prefix, context)


@public
def put_on_storage(key: Union[str, bytes], value: Union[int, str, bytes]):
    put(key, value)
