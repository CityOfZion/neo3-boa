from boa3.builtin import public
from boa3.builtin.interop.contract import NEO
from boa3.builtin.type import UInt160


@public
def Main() -> UInt160:
    return NEO
