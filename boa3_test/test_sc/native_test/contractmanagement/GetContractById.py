from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement
from boa3.sc.types import Contract


@public
def main(contract_id: int) -> Contract | None:
    return ContractManagement.get_contract_by_id(contract_id)
