from boa3.builtin.compile_time import public
from boa3.builtin.interop import storage
from boa3.builtin.interop.iterator import Iterator


@public
def put_value(key: bytes, value: int):
    storage.put_int(key, value)


@public
def get_value(key: bytes) -> int:
    return storage.get_int(key)


@public
def delete_value(key: bytes):
    storage.delete(key)


@public
def find_by_prefix(prefix: bytes) -> Iterator:
    return storage.find(prefix)
