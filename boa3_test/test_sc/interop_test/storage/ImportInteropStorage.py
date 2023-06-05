from boa3.builtin import interop
from boa3.builtin.compile_time import public
from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.type.helper import to_int


@public
def put_value(key: str, value: int):
    interop.storage.put(key, value)


@public
def get_value(key: str) -> int:
    return to_int(interop.storage.get(key))


@public
def delete_value(key: str):
    interop.storage.delete(key)


@public
def find_by_prefix(prefix: str) -> Iterator:
    return interop.storage.find(prefix)


@public
def create_storage_map(prefix: str) -> interop.storage.StorageMap:
    return interop.storage.get_context().create_map(prefix)
