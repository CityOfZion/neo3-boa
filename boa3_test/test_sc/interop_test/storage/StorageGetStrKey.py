from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop import storage
from boa3.builtin.interop.storage import get


@public
def Main(key: str) -> bytes:
    return get(key)


@public
def _deploy(data: Any, update: bool):
    # test data to test in unit tests
    storage.put('example', 23)
    storage.put('test', 42)
