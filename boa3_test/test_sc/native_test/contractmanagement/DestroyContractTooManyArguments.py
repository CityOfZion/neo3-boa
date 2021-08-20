from typing import Any

from boa3.builtin.nativecontract.contractmanagement import ContractManagement


def Main(arg0: Any):
    ContractManagement.destroy(arg0)
