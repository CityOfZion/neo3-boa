from boa3.builtin import public
from boa3.builtin.interop import storage
from boa3.builtin.interop.iterator import Iterator


@public
def put_value(key: str, value: int):
    storage.put(key, value)


@public
def get_value(key: str) -> int:
    return storage.get(key).to_int()


@public
def delete_value(key: str):
    storage.delete(key)


@public
def find_by_prefix(prefix: str) -> Iterator:
    return storage.find(prefix)
