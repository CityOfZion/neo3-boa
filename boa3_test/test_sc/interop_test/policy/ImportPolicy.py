from boa3.builtin.interop import policy
from boa3.sc.compiletime import public


@public
def main() -> int:
    return policy.get_exec_fee_factor()
