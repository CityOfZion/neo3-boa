from boa3.builtin.interop.contract import GAS
from boa3.sc.compiletime import public
from boa3.sc.types import UInt160


@public
def Main() -> UInt160:
    return GAS
