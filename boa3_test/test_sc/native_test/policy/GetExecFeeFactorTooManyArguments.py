from boa3.sc.contracts import PolicyContract


def main() -> int:
    return PolicyContract.get_exec_fee_factor(10)
