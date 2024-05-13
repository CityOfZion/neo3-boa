from boa3.sc import runtime
from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement
from boa3.sc.types import Contract


@public
def main() -> str | None:
    current_script = runtime.executing_script_hash
    contract: Contract = ContractManagement.get_contract(current_script)
    if not isinstance(contract, Contract):
        return None

    contract_name = contract.manifest.name
    return contract_name
