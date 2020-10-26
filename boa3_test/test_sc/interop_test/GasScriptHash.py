from boa3.builtin import public
from boa3.builtin.interop.contract import GAS


@public
def Main() -> bytes:
    return GAS
