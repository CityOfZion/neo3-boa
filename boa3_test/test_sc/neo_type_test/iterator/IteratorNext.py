from boa3.sc import storage
from boa3.sc.compiletime import public


@public
def has_next(prefix: bytes) -> bool:
    return storage.find(prefix).next()


@public
def store_data(key: bytes, value: int):
    storage.put_int(key, value)
