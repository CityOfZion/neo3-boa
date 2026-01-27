from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.storage import get_context, find, put


@public
def _deploy(data: Any, update: bool):
    put(b'data1', b"fizz")
    put(b'data2', b"buzz")
    put(b'data3', b"unit")
    put(b'data4', b"test")


@public
def find_local(prefix: bytes) -> list[Any]:
    iterator = find(prefix)
    list_ = []
    for key in iterator:
        list_.append(key)
    return list_


@public
def find_context(prefix: bytes) -> list[Any]:
    iterator = find(prefix, get_context().as_read_only())
    list_ = []
    for key in iterator:
        list_.append(key)
    return list_
