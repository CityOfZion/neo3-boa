from boa3.builtin.compile_time import public
from boa3.builtin.interop.policy import get_exec_fee_factor


@public
def main() -> int:
    return get_exec_fee_factor()
