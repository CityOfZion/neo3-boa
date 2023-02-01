from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop import storage
from boa3.builtin.interop.storage import get, get_context
from boa3.builtin.type import ByteString


@public
def Main(key: ByteString) -> bytes:
    context = get_context()
    return get(key, context)


@public
def _deploy(data: Any, update: bool):
    # test data to test in unit tests
    context = get_context()
    storage.put('example', 23, context)
    storage.put('test', 42, context)

