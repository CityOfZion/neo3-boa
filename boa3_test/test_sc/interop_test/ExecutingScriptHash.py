from boa3.builtin import public
from boa3.builtin.interop.runtime import executing_script_hash


@public
def Main() -> bytes:
    return executing_script_hash
