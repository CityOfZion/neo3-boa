from typing import Any

from boa3.sc.contracts import ContractManagement


def Main(arg0: Any):
    ContractManagement.destroy(arg0)
