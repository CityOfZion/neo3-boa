from typing import Any

from boa3.sc.contracts import ContractManagement


def Main(script: bytes, manifest: str, data: Any, arg0: Any):
    ContractManagement.update(script, manifest, data, arg0)
