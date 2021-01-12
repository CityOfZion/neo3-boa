from boa3.builtin.interop.contract import GAS
from boa3.builtin.type import UInt160


def Main(example: UInt160) -> UInt160:
    global GAS
    GAS = example
    return GAS
