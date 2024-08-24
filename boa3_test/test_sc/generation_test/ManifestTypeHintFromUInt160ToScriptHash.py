from boa3.sc.compiletime import public
from boa3.sc.types import ScriptHash
from boa3.sc.utils import to_script_hash


@public
def Main() -> ScriptHash:
    return to_script_hash(123)
