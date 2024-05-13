from boa3.sc.compiletime import public
from boa3.builtin.interop.contract import NEO
from boa3.sc.types import UInt160


@public
def Main() -> UInt160:
    return NEO
