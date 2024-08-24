from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement
from boa3.sc.types import Contract


@public
def Main(script: bytes, manifest: bytes, data: Any) -> Contract:
    return ContractManagement.deploy(script, manifest, data)
