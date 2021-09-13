from boa3.builtin.nativecontract.policy import Policy


def main() -> int:
    return Policy.is_blocked('str')
