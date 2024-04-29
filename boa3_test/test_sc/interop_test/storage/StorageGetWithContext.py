from typing import Any

from boa3.builtin.compile_time import public
from boa3.sc import storage
from boa3.sc.storage import get, get_context


@public
def Main(key: bytes) -> bytes:
    context = get_context()
    return get(key, context)


@public
def _deploy(data: Any, update: bool):
    # test data to test in unit tests
    context = get_context()
    storage.put_int(b'example', 23, context)
    storage.put_int(b'test', 42, context)
