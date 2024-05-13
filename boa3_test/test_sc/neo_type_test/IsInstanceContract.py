from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement
from boa3.sc.runtime import executing_script_hash
from boa3.sc.types import Contract


@public
def is_contract(value: Any) -> bool:
    return isinstance(value, Contract)


@public
def is_get_contract_a_contract() -> bool:
    contract = ContractManagement.get_contract(executing_script_hash)
    return is_contract(contract)
