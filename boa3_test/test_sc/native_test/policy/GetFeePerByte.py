from boa3.builtin import public
from boa3.builtin.nativecontract.policy import Policy


@public
def main() -> int:
    return Policy.get_fee_per_byte()
