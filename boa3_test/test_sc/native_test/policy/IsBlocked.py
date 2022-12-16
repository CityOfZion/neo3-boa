from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.policy import Policy
from boa3.builtin.type import UInt160


@public
def main(account: UInt160) -> int:
    return Policy.is_blocked(account)
