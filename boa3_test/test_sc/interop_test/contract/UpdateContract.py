from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement


@public
def update(script: bytes, manifest: bytes, data: Any):
    ContractManagement.update(script, manifest, data)
