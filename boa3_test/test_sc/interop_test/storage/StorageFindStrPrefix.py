from boa3.sc.storage import find, put
from boa3.sc.utils.iterator import Iterator


def find_by_prefix(prefix: str) -> Iterator:
    return find(prefix)


def put_on_storage(key: bytes, value: bytes):
    put(key, value)
