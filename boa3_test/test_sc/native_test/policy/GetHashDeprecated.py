from boa3.sc.compiletime import public
from boa3.builtin.nativecontract.policy import Policy
from boa3.sc.types import UInt160


@public
def main() -> UInt160:
    return Policy.hash
