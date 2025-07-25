from boa3.sc.compiletime import public
from boa3.sc.storage import StorageMap, get_context


@public
def get_from_map(key: bytes) -> bytes:
    context = create_map()
    return context.get(key)


@public
def insert_to_map(key: bytes, value: bytes):
    context = create_map()
    context.put(key, value)


@public
def delete_from_map(key: bytes):
    context = create_map()
    context.delete(key)


def create_map() -> StorageMap:
    return get_context().create_map(b'example_')
