from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import get, put


@public
def get_value(key: str) -> int:
    return get(key).to_int()


@public
def put_value(key: str, value: int):
    put(key, value)
