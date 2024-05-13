from boa3.sc.compiletime import public
from boa3.sc.types import ScriptHashLittleEndian
from boa3.sc.utils import to_script_hash


@public
def Main() -> ScriptHashLittleEndian:
    return to_script_hash(123)
