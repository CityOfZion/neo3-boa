from boa3.sc.contracts import PolicyContract


def main() -> int:
    return PolicyContract.get_fee_per_byte(10)
