from boa3.builtin.compile_time import public
from boa3.builtin.contract import to_script_hash
from boa3.builtin.type import ScriptHash


@public
def Main() -> ScriptHash:
    return to_script_hash(123)
