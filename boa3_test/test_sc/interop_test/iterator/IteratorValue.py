from boa3.sc.compiletime import public
from boa3.sc import storage


@public
def test_iterator(prefix: bytes) -> tuple | None:
    it = storage.find(prefix)
    if it.next():
        return it.value
    return None


@public
def store_data(key: bytes, value: int):
    storage.put_int(key, value)
