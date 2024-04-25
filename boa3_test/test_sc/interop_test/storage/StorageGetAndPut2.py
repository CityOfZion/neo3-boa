from boa3.builtin.compile_time import public
from boa3.sc.storage import get_int, put_int


@public
def get_value(key: bytes) -> int:
    return get_int(key)


@public
def put_value(key: bytes, value: int):
    put_int(key, value)
