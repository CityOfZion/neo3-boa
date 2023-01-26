from boa3.builtin.compile_time import public
from boa3.builtin.type import ScriptHashLittleEndian, UInt160


@public
def main() -> ScriptHashLittleEndian:
    return ScriptHashLittleEndian(UInt160())
