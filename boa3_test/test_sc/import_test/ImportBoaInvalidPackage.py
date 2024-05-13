from boa3.internal.neo import to_script_hash  # should not be imported
from boa3.sc.compiletime import public


@public
def Main() -> bytes:
    return to_script_hash(b'42')
