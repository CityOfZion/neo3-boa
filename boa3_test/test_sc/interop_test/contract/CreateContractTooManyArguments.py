from typing import Any

from boa3.sc.contracts import ContractManagement


def Main(script: bytes, manifest: bytes, data: Any, arg0: Any):
    ContractManagement.deploy(script, manifest, data, arg0)
