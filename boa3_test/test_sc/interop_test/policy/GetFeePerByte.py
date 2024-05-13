from boa3.sc.compiletime import public
from boa3.sc.contracts import PolicyContract


@public
def main() -> int:
    return PolicyContract.get_fee_per_byte()
