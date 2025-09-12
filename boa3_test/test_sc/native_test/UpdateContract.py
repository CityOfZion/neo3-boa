from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement
from boa3.sc.runtime import notify


@public
def update(script: bytes, manifest: bytes, data: Any):
    ContractManagement.update(script, manifest, data)


@public
def new_method() -> int:
    return 42


@public
def _deploy(data: Any, update: bool):
    notify(update)
    notify(data)
