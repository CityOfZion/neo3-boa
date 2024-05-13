from boa3.sc.compiletime import public
from boa3.sc.types import ScriptHash, UInt160


@public
def main() -> ScriptHash:
    return ScriptHash(UInt160())
