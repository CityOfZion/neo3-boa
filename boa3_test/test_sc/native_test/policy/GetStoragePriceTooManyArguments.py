from boa3.builtin.nativecontract.policy import Policy


def main() -> int:
    return Policy.get_storage_price(123)
