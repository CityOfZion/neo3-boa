from boa3.sc.compiletime import public
from boa3.sc.storage import get_int, put_int


@public
def put_value(key: bytes, value: int):
    put_int(key, value)


@public
def get_value(key: bytes) -> int:
    return get_int(key)
