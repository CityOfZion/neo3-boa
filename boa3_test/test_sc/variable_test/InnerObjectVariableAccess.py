from typing import Optional

from boa3.builtin.compile_time import public
from boa3.builtin.interop import runtime
from boa3.builtin.interop.contract import Contract
from boa3.builtin.nativecontract.contractmanagement import ContractManagement


@public
def main() -> Optional[str]:
    current_script = runtime.executing_script_hash
    contract: Contract = ContractManagement.get_contract(current_script)
    if not isinstance(contract, Contract):
        return None

    contract_name = contract.manifest.name
    return contract_name
