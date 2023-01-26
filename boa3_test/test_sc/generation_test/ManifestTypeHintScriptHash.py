from boa3.builtin.compile_time import public
from boa3.builtin.type import ScriptHash, UInt160


@public
def main() -> ScriptHash:
    return ScriptHash(UInt160())
