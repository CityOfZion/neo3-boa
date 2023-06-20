from boa3.builtin.compile_time import public
from boa3.builtin.interop import storage


@public
def has_next(prefix: bytes) -> bool:
    return storage.find(prefix).next()


@public
def store_data(key: bytes, value: int):
    storage.put(key, value)
