from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop import storage, runtime


@public
def _deploy(data: Any, update: bool):
    if not update:
        storage.put(b'testKey', runtime.executing_script_hash)


@public
def get_script() -> bytes:
    return storage.get(b'testKey')
