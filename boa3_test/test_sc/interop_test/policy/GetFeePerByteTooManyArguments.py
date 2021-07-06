from boa3.builtin.interop.policy import get_fee_per_byte


def main() -> int:
    return get_fee_per_byte(10)
