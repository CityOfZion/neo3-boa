from boa3.builtin.compile_time import public
from boa3.builtin.interop.iterator import Iterator
from boa3.sc.storage import find, put


@public
def find_by_prefix(prefix: bytes) -> Iterator:
    return find(prefix)


@public
def put_on_storage(key: bytes, value: bytes):
    put(key, value)
