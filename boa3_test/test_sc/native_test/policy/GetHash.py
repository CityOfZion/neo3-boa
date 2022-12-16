from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.policy import Policy
from boa3.builtin.type import UInt160


@public
def main() -> UInt160:
    return Policy.hash
