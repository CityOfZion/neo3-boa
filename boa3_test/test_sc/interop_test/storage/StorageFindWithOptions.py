from typing import Union

from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.interop.storage import find, get_context, put
from boa3.builtin.interop.storage.findoptions import FindOptions
from boa3.builtin.type import ByteString


@public
def find_by_prefix(prefix: ByteString) -> Iterator:
    context = get_context()
    return find(prefix, context, FindOptions.REMOVE_PREFIX)


@public
def put_on_storage(key: ByteString, value: Union[int, ByteString]):
    put(key, value)
