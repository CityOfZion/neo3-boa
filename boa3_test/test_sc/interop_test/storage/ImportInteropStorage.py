from boa3.builtin import interop
from boa3.builtin.compile_time import public
from boa3.builtin.interop.iterator import Iterator


@public
def put_value(key: bytes, value: int):
    interop.storage.put_int(key, value)


@public
def get_value(key: bytes) -> int:
    return interop.storage.get_int(key)


@public
def delete_value(key: bytes):
    interop.storage.delete(key)


@public
def find_by_prefix(prefix: bytes) -> Iterator:
    return interop.storage.find(prefix)


@public
def create_storage_map(prefix: bytes) -> interop.storage.StorageMap:
    return interop.storage.get_context().create_map(prefix)
