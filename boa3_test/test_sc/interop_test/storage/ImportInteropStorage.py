from boa3.builtin import interop, public
from boa3.builtin.interop.iterator import Iterator


@public
def put_value(key: str, value: int):
    interop.storage.put(key, value)


@public
def get_value(key: str) -> int:
    return interop.storage.get(key).to_int()


@public
def delete_value(key: str):
    interop.storage.delete(key)


@public
def find_by_prefix(prefix: str) -> Iterator:
    return interop.storage.find(prefix)


@public
def create_storage_map(prefix: str) -> interop.storage.StorageMap:
    return interop.storage.get_context().create_map(prefix)
