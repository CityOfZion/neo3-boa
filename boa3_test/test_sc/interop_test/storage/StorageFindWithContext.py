from boa3.sc.compiletime import public
from boa3.sc.storage import find, get_context, put
from boa3.sc.utils.iterator import Iterator


@public
def find_by_prefix(prefix: bytes) -> Iterator:
    context = get_context()
    return find(prefix, context)


@public
def put_on_storage(key: bytes, value: bytes):
    put(key, value)
