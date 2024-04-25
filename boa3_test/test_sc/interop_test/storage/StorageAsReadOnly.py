from boa3.builtin.compile_time import public
from boa3.sc.storage import get_str, get_context, put_str


@public
def put_value_in_storage(key: bytes, value: str):
    put_str(key, value)


@public
def get_value_in_storage(key: bytes) -> str:
    return get_str(key)


@public
def put_value_in_storage_read_only(key: bytes, value: str):
    put_str(key, value, get_context().as_read_only())


@public
def get_value_in_storage_read_only(key: bytes) -> str:
    return get_str(key, get_context().as_read_only())
