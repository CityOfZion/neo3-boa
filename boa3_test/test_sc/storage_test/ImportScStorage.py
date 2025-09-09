from boa3 import sc
from boa3.sc.compiletime import public
from boa3.sc.utils.iterator import Iterator


@public
def put_value(key: bytes, value: int):
    sc.storage.put_int(key, value)


@public
def get_value(key: bytes) -> int:
    return sc.storage.get_int(key)


@public
def delete_value(key: bytes):
    sc.storage.delete(key)


@public
def find_by_prefix(prefix: bytes) -> Iterator:
    return sc.storage.find(prefix)


@public
def create_storage_map(prefix: bytes) -> sc.storage.StorageMap:
    return sc.storage.get_context().create_map(prefix)
