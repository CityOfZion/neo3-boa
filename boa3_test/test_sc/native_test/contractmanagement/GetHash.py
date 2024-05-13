from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement
from boa3.sc.types import UInt160


@public
def main() -> UInt160:
    return ContractManagement.hash
