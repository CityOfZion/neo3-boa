from boa3.builtin import public
from boa3.builtin.interop.storage import get, get_context, put


@public
def put_value_in_storage(key: str, value: str):
    put(key, value)


@public
def get_value_in_storage(key: str) -> str:
    return get(key).to_str()


@public
def put_value_in_storage_read_only(key: str, value: str):
    put(key, value, get_context().as_read_only())


@public
def get_value_in_storage_read_only(key: str) -> str:
    return get(key, get_context().as_read_only()).to_str()
