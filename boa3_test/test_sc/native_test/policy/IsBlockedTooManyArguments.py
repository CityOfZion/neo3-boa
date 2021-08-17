from boa3.builtin.nativecontract.policy import Policy
from boa3.builtin.type import UInt160


def main() -> int:
    return Policy.is_blocked(UInt160(), UInt160())
