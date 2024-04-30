from boa3.builtin.compile_time import public
from boa3.sc.storage import try_get_int, put_int


@public
def put_value(key: bytes, value: int):
    put_int(key, value)


@public
def get_value(key: bytes) -> bool:
    return try_get_int(key)[1]
