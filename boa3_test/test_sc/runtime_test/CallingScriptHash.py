from boa3.sc.compiletime import public
from boa3.sc.runtime import calling_script_hash
from boa3.sc.types import UInt160


@public
def Main() -> UInt160:
    return calling_script_hash
