from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.storage import get_context, delete, put, get


@public
def get_value(key: bytes) -> bytes:
    return get(key)


@public
def _deploy(data: Any, update: bool):
    put(b'data1', b"fizz")
    put(b'data2', b"buzz")


@public
def delete_local(prefix: bytes) -> None:
    return delete(prefix)


@public
def delete_context(prefix: bytes) -> None:
    return delete(prefix, get_context())
