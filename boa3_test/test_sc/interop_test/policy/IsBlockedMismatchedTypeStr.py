from boa3.sc.contracts import PolicyContract


def main() -> int:
    return PolicyContract.is_blocked('str')
