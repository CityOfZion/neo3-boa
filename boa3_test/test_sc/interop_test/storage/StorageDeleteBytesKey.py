from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop import storage
from boa3.builtin.interop.storage import delete


@public
def Main(key: bytes):
    delete(key)


@public
def has_key(key: bytes) -> bool:
    return len(storage.get(key)) > 0


@public
def _deploy(data: Any, update: bool):
    # test data to test in unit tests
    storage.put(b'example', 23)
