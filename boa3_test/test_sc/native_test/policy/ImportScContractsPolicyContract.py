from boa3 import sc
from boa3.sc.compiletime import public


@public
def main() -> int:
    return sc.contracts.PolicyContract.get_exec_fee_factor()
