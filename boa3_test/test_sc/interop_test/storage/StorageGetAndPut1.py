from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import get, put
from boa3.builtin.type.helper import to_int


@public
def put_value(key: bytes, value: int):
    put(key, value)


@public
def get_value(key: bytes) -> int:
    return to_int(get(key))
