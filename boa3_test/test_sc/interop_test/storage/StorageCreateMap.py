from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import StorageMap, get_context


@public
def get_from_map(key: str) -> bytes:
    context = create_map()
    return context.get(key)


@public
def insert_to_map(key: str, value: str):
    context = create_map()
    context.put(key, value)


@public
def delete_from_map(key: str):
    context = create_map()
    context.delete(key)


def create_map() -> StorageMap:
    return get_context().create_map('example_')
