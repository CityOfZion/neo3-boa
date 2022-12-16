from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.contractmanagement import ContractManagement


@public
def update(script: bytes, manifest: bytes, data: Any):
    ContractManagement.update(script, manifest, data)
