from boa3.builtin import public
from boa3.builtin.interop import policy


@public
def main() -> int:
    return policy.get_exec_fee_factor()
