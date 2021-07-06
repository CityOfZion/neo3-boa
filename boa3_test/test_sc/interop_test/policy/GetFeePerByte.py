from boa3.builtin import public
from boa3.builtin.interop.policy import get_fee_per_byte


@public
def main() -> int:
    return get_fee_per_byte()
