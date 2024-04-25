from boa3.builtin.compile_time import public
from boa3.builtin.interop.iterator import Iterator
from boa3.sc.storage import find, get_context, put
from boa3.sc.types.findoptions import FindOptions


@public
def find_by_prefix(prefix: bytes) -> Iterator:
    context = get_context()
    return find(prefix, context, FindOptions.REMOVE_PREFIX)


@public
def put_on_storage(key: bytes, value: bytes):
    put(key, value)
