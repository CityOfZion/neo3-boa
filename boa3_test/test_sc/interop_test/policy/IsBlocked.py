from boa3.builtin.compile_time import public
from boa3.builtin.interop.policy import is_blocked
from boa3.builtin.type import UInt160


@public
def main(account: UInt160) -> int:
    return is_blocked(account)
