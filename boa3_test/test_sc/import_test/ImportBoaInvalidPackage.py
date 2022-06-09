from boa3.builtin import public
from boa3.neo import to_script_hash  # should not be imported


@public
def Main() -> bytes:
    return to_script_hash(b'42')
