from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop import runtime
from boa3.builtin.type import UInt160
from boa3.sc import storage


@public
def _deploy(data: Any, update: bool):
    if not update:
        storage.put_uint160(b'testKey', runtime.executing_script_hash)


@public
def get_script() -> UInt160:
    return storage.get_uint160(b'testKey')
