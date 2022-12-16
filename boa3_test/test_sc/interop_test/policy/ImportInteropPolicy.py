from boa3.builtin import interop
from boa3.builtin.compile_time import public


@public
def main() -> int:
    return interop.policy.get_exec_fee_factor()
