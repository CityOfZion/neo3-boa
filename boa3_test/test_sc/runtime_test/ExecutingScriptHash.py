from boa3.sc.compiletime import public
from boa3.sc.runtime import executing_script_hash
from boa3.sc.types import UInt160


@public
def Main() -> UInt160:
    return executing_script_hash
