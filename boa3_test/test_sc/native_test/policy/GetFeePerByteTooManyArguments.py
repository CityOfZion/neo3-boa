from boa3.builtin.nativecontract.policy import Policy


def main() -> int:
    return Policy.get_fee_per_byte(10)
