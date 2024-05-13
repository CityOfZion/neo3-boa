from boa3.sc.compiletime import public
from boa3.builtin.interop.contract import GAS
from boa3.sc.types import UInt160


@public
def Main(example: UInt160) -> UInt160:
    GAS = example
    return GAS


def interop_call():
    x = GAS
