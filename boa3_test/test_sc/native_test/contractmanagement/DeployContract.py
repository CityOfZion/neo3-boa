from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import Contract
from boa3.builtin.nativecontract.contractmanagement import ContractManagement


@public
def Main(script: bytes, manifest: bytes, data: Any) -> Contract:
    return ContractManagement.deploy(script, manifest, data)
