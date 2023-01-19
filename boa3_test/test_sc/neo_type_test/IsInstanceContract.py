from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import get_contract
from boa3.builtin.interop.contract.contract import Contract
from boa3.builtin.interop.runtime import executing_script_hash


@public
def is_contract(value: Any) -> bool:
    return isinstance(value, Contract)


@public
def is_get_contract_a_contract() -> bool:
    contract = get_contract(executing_script_hash)
    return is_contract(contract)
