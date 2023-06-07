from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import get, get_context, put
from boa3.builtin.type.helper import to_str


@public
def put_value_in_storage(key: bytes, value: str):
    put(key, value)


@public
def get_value_in_storage(key: bytes) -> str:
    return to_str(get(key))


@public
def put_value_in_storage_read_only(key: bytes, value: str):
    put(key, value, get_context().as_read_only())


@public
def get_value_in_storage_read_only(key: bytes) -> str:
    return to_str(get(key, get_context().as_read_only()))
