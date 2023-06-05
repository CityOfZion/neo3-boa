from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop import storage
from boa3.builtin.interop.storage import delete, get_context


@public
def Main(key: bytes):
    context = get_context()
    delete(key, context)


@public
def has_key(key: bytes) -> bool:
    context = get_context()
    return len(storage.get(key, context)) > 0


@public
def _deploy(data: Any, update: bool):
    # test data to test in unit tests
    context = get_context()
    storage.put(b'example', 23, context)
