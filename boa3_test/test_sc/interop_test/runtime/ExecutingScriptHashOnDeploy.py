from typing import Any

from boa3.sc import runtime, storage
from boa3.sc.compiletime import public


@public
def _deploy(data: Any, update: bool):
    if not update:
        storage.put_uint160(b'testKey', runtime.executing_script_hash)


@public
def get_script() -> bytes:
    return storage.get(b'testKey')
