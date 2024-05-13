from boa3.sc.contracts import PolicyContract


def main() -> int:
    return PolicyContract.get_storage_price(123)
