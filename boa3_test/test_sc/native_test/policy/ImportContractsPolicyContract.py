from boa3.sc import contracts
from boa3.sc.compiletime import public


@public
def main() -> int:
    return contracts.PolicyContract.get_exec_fee_factor()
