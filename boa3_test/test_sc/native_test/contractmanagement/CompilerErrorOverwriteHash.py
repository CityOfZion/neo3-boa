from boa3.sc.contracts import ContractManagement
from boa3.sc.types import UInt160


def main() -> UInt160:
    ContractManagement.hash = UInt160()
    return ContractManagement.hash
