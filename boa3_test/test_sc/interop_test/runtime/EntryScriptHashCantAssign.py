from boa3.sc.compiletime import public
from boa3.sc.runtime import entry_script_hash
from boa3.sc.types import UInt160


@public
def main(example: UInt160) -> UInt160:
    entry_script_hash = example
    return entry_script_hash


def interop_call():
    x = entry_script_hash
