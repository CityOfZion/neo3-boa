from boa3.sc.compiletime import public
from boa3.sc.types import ScriptHashLittleEndian, UInt160


@public
def main() -> ScriptHashLittleEndian:
    return ScriptHashLittleEndian(UInt160())
