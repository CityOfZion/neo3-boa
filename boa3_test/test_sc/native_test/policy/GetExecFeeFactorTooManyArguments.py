from boa3.builtin.nativecontract.policy import Policy


def main() -> int:
    return Policy.get_exec_fee_factor(10)
