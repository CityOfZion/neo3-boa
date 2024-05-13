from boa3.sc.compiletime import public
from boa3.sc.storage import find, put
from boa3.sc.utils.iterator import Iterator


@public
def find_by_prefix(prefix: bytes) -> Iterator:
    return find(prefix)


@public
def put_on_storage(key: bytes, value: bytes):
    put(key, value)
