from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import update_contract
from boa3.builtin.interop.runtime import notify


@public
def update(script: bytes, manifest: bytes, data: Any):
    update_contract(script, manifest, data)


@public
def new_method() -> int:
    return 42


@public
def _deploy(data: Any, update: bool):
    notify(update)
    notify(data)
