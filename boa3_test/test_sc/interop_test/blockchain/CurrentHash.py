from boa3.sc.compiletime import public
from boa3.builtin.interop.blockchain import current_hash
from boa3.sc.types import UInt256


@public
def main() -> UInt256:
    return current_hash
