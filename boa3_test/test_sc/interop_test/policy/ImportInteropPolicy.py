from boa3.builtin import interop, public


@public
def main() -> int:
    return interop.policy.get_exec_fee_factor()
