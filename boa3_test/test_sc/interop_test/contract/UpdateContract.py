from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import update_contract


@public
def update(script: bytes, manifest: bytes, data: Any):
    update_contract(script, manifest, data)
