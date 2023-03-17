from boa3.builtin.compile_time import public
from boa3.internal.neo import to_script_hash  # should not be imported


@public
def Main() -> bytes:
    return to_script_hash(b'42')
