from boa3.sc.contracts import PolicyContract
from boa3.sc.types import UInt160


def main() -> UInt160:
    PolicyContract.hash = UInt160()
    return PolicyContract.hash
