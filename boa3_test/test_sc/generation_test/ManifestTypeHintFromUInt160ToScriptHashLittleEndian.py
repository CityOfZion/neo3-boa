from boa3.builtin.compile_time import public
from boa3.builtin.type import ScriptHashLittleEndian


@public
def Main() -> ScriptHashLittleEndian:
    return int.to_script_hash(123)
