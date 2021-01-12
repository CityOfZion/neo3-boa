from boa3.builtin import public
from boa3.builtin.interop.contract import GAS
from boa3.builtin.type import UInt160


@public
def Main() -> UInt160:
    return GAS
