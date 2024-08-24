from boa3.sc.compiletime import public
from boa3.sc.runtime import entry_script_hash
from boa3.sc.types import UInt160


@public
def main() -> UInt160:
    return entry_script_hash
