from boa3.sc.contracts import PolicyContract
from boa3.sc.types import UInt160


def main() -> int:
    return PolicyContract.is_blocked(UInt160(), UInt160())
