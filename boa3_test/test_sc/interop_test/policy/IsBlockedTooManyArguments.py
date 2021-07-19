from boa3.builtin.interop.policy import is_blocked
from boa3.builtin.type import UInt160


def main() -> int:
    return is_blocked(UInt160(), UInt160())
