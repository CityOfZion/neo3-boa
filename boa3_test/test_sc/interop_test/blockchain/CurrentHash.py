from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import current_hash
from boa3.builtin.type import UInt256


@public
def main() -> UInt256:
    return current_hash
