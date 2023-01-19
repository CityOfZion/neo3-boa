from boa3.builtin.compile_time import public
from boa3.builtin.type import ScriptHash


@public
def Main() -> ScriptHash:
    return int.to_script_hash(123)
