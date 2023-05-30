from boa3.builtin.compile_time import public
from boa3.builtin.contract import to_script_hash


@public
def Main() -> bytes:
    return to_script_hash(123)
