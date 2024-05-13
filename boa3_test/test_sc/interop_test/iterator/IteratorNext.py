from boa3.sc.compiletime import public
from boa3.sc import storage


@public
def has_next(prefix: bytes) -> bool:
    return storage.find(prefix).next()


@public
def store_data(key: bytes, value: int):
    storage.put_int(key, value)
