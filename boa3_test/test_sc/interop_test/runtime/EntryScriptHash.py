from boa3.builtin import public
from boa3.builtin.interop.runtime import entry_script_hash
from boa3.builtin.type import UInt160


@public
def main() -> UInt160:
    return entry_script_hash
